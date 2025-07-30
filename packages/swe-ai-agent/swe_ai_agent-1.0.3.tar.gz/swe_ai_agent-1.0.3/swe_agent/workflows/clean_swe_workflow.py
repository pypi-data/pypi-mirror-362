"""
Clean SWE Workflow implementation following LangGraph best practices.
Removes hardcoding and uses tool-based approach with proper prompts.
"""

import operator
import logging
import traceback
from typing import Annotated, Literal, Sequence, TypedDict, Dict, Any
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, ToolMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.graph import END, START, StateGraph
from langgraph.prebuilt import ToolNode
from pathlib import Path
from tenacity import retry, stop_after_attempt, wait_exponential

from prompts.swe_prompts import SOFTWARE_ENGINEER_PROMPT, CODE_ANALYZER_PROMPT, EDITING_AGENT_PROMPT
from langchain_anthropic import ChatAnthropic
from tools.langraph_tools import LangGraphTools
from tools.advanced_langraph_tools import AdvancedLangGraphTools
from tools.planning_tools import PlanningTools
from agents.planner import PlannerAgent
from state.agent_state import AgentState, create_initial_state

logger = logging.getLogger(__name__)

class CleanSWEWorkflow:
    """
    Clean SWE Workflow implementation following LangGraph best practices.
    Uses tool-based agents with proper prompts instead of hardcoded logic.
    """
    
    def __init__(self, repo_path: str, output_dir: str, use_planner: bool = False):
        self.repo_path = Path(repo_path)
        self.output_dir = Path(output_dir)
        self.use_planner = use_planner  # Feature flag for planner logic
        
        # Initialize Claude client for LangChain
        # The newest Anthropic model is "claude-sonnet-4-20250514", not "claude-3-7-sonnet-20250219", "claude-3-5-sonnet-20241022" nor "claude-3-sonnet-20240229"
        self.anthropic_client = ChatAnthropic(
            model="claude-sonnet-4-20250514",
            temperature=0,
            max_tokens=4096
        )
        
        # Initialize tools
        self.langraph_tools = LangGraphTools(str(repo_path))
        self.advanced_tools = AdvancedLangGraphTools(str(repo_path))
        
        # Initialize Planner Agent only if enabled
        if self.use_planner:
            self.planning_tools = PlanningTools()
            self.planner_agent = PlannerAgent(self.planning_tools)
        else:
            self.planning_tools = None
            self.planner_agent = None
        
        # All agents get access to all 20 tools for maximum flexibility
        all_tools = self.advanced_tools.get_all_tools()
        
        # Give all agents access to all tools
        self.all_agent_tools = all_tools
        
        # Create unified tool node for all agents
        self.unified_tool_node = ToolNode(all_tools)
        
        # Agent names
        self.planner_name = "Planner"
        self.software_engineer_name = "SoftwareEngineer"
        self.code_analyzer_name = "CodeAnalyzer"
        self.editor_name = "Editor"
        
        # Build the workflow
        self.workflow = self._build_workflow()
        
        planner_status = "enabled" if self.use_planner else "disabled"
        logger.info(f"🔧 Clean SWE Workflow initialized with Planner {planner_status} and {len(all_tools)} tools")
    
    def _create_agent(self, system_prompt: str, tools: list):
        """Create an agent with system prompt and tools."""
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="messages"),
        ])
        
        llm = self.anthropic_client
        if tools:
            return prompt | llm.bind_tools(tools)
        else:
            return prompt | llm
    
    def _create_agent_node(self, agent, name: str):
        """Create an agent node for the workflow following the reference pattern."""
        def agent_node(state):
            @retry(
                stop=stop_after_attempt(3),
                wait=wait_exponential(multiplier=1, min=4, max=10),
            )
            def invoke_with_retry(agent, state):
                return agent.invoke(state)

            try:
                # Track consecutive visits to prevent infinite loops
                consecutive_visits = state.get("consecutive_visits", {})
                visit_count = consecutive_visits.get(name, 0) + 1
                consecutive_visits[name] = visit_count
                
                result = invoke_with_retry(agent, state)
                
            except Exception as e:
                logger.error(f"Failed to invoke {name} agent after 3 attempts: {traceback.format_exc()}")
                result = AIMessage(
                    content=f"I apologize, but I encountered an error and couldn't complete the task. Please try again or rephrase your request.".rstrip(),
                    name=name,
                )
                consecutive_visits = state.get("consecutive_visits", {})
                consecutive_visits[name] = consecutive_visits.get(name, 0) + 1
            
            # Handle different result types following reference pattern
            if not isinstance(result, ToolMessage):
                if isinstance(result, dict):
                    result_dict = result
                else:
                    result_dict = result.dict() if hasattr(result, 'dict') else {
                        'content': str(result.content) if hasattr(result, 'content') else str(result),
                        'tool_calls': getattr(result, 'tool_calls', [])
                    }
                
                # Fix: Strip trailing whitespace from content to prevent Anthropic API errors
                if 'content' in result_dict and isinstance(result_dict['content'], str):
                    result_dict['content'] = result_dict['content'].rstrip()
                
                result = AIMessage(
                    **{
                        k: v
                        for k, v in result_dict.items()
                        if k not in ["type", "name"]
                    },
                    name=name,
                )
            
            return {
                "messages": [result], 
                "sender": name,
                "consecutive_visits": consecutive_visits
            }
        
        return agent_node
    
    def _build_workflow(self) -> StateGraph:
        """Build the clean workflow graph with Planner approval."""
        # Create agents - all agents get access to all tools
        software_engineer_agent = self._create_agent(SOFTWARE_ENGINEER_PROMPT, self.all_agent_tools)
        code_analyzer_agent = self._create_agent(CODE_ANALYZER_PROMPT, self.all_agent_tools)
        editing_agent = self._create_agent(EDITING_AGENT_PROMPT, self.all_agent_tools)
        
        # Create agent nodes
        planner_node = self._create_planner_node()
        software_engineer_node = self._create_agent_node(software_engineer_agent, self.software_engineer_name)
        code_analyzer_node = self._create_agent_node(code_analyzer_agent, self.code_analyzer_name)
        editing_node = self._create_agent_node(editing_agent, self.editor_name)
        
        # Create workflow
        workflow = StateGraph(AgentState)
        
        # Add nodes
        if self.use_planner:
            workflow.add_node(self.planner_name, planner_node)
        workflow.add_node(self.software_engineer_name, software_engineer_node)
        workflow.add_node(self.code_analyzer_name, code_analyzer_node)
        workflow.add_node(self.editor_name, editing_node)
        workflow.add_node("tools", self.unified_tool_node)
        
        # Set entry point based on feature flag
        if self.use_planner:
            workflow.add_edge(START, self.planner_name)
        else:
            workflow.add_edge(START, self.software_engineer_name)
        
        # Add unified tool routing - all agents can use all tools
        workflow.add_conditional_edges(
            "tools",
            lambda x: x["sender"],
            {
                self.software_engineer_name: self.software_engineer_name,
                self.code_analyzer_name: self.code_analyzer_name,
                self.editor_name: self.editor_name,
            },
        )
        
        # Add Planner routing only if enabled
        if self.use_planner:
            workflow.add_conditional_edges(
                self.planner_name,
                self._planner_router,
                {
                    "approved": self.software_engineer_name,
                    "rejected": END,
                    "continue": self.planner_name,
                },
            )
        
        # Add main routing logic
        workflow.add_conditional_edges(
            self.software_engineer_name,
            self._software_engineer_router,
            {
                "continue": self.software_engineer_name,
                "analyze_code": self.code_analyzer_name,
                "edit_file": self.editor_name,
                "tools": "tools",
                "__end__": END,
            },
        )
        
        workflow.add_conditional_edges(
            self.code_analyzer_name,
            self._code_analyzer_router,
            {
                "continue": self.code_analyzer_name,
                "done": self.software_engineer_name,
                "edit_file": self.editor_name,
                "tools": "tools",
            },
        )
        
        workflow.add_conditional_edges(
            self.editor_name,
            self._editor_router,
            {
                "continue": self.editor_name,
                "done": self.software_engineer_name,
                "tools": "tools",
            },
        )
        
        return workflow
    
    def _create_planner_node(self):
        """Create the Planner agent node."""
        def planner_node(state):
            try:
                # Track consecutive visits to prevent infinite loops
                consecutive_visits = state.get("consecutive_visits", {})
                visit_count = consecutive_visits.get(self.planner_name, 0) + 1
                consecutive_visits[self.planner_name] = visit_count
                
                # Use the planner agent to evaluate and approve tasks
                messages = state.get("messages", [])
                if messages:
                    # Let the planner agent assess the task and create a plan
                    result = self.planner_agent.process(state)
                    
                    # Check if planner has created an approvable plan
                    last_message = result.get("messages", [])[-1] if result.get("messages") else None
                    if last_message and any(signal in last_message.content.lower() for signal in ["plan approved", "proceeding with implementation", "implementation ready"]):
                        # Auto-approve to move to software engineer
                        approval_msg = AIMessage(
                            content="Plan approved. Proceeding with implementation.".rstrip(),
                            name=self.planner_name
                        )
                        return {
                            "messages": result.get("messages", []) + [approval_msg],
                            "sender": self.planner_name,
                            "consecutive_visits": consecutive_visits
                        }
                    
                    # Add consecutive visits to result and return
                    result["consecutive_visits"] = consecutive_visits
                    return result
            except Exception as e:
                logger.error(f"Error in Planner agent: {e}")
                error_msg = AIMessage(
                    content=f"Error in Planner: {str(e)}".rstrip(),
                    name=self.planner_name
                )
                return {
                    "messages": [error_msg], 
                    "sender": self.planner_name,
                    "consecutive_visits": consecutive_visits
                }
        
        return planner_node
    
    def _planner_router(self, state) -> Literal["approved", "rejected", "continue"]:
        """Route from Planner based on approval status."""
        messages = state["messages"]
        
        # Find the last AI message
        for message in reversed(messages):
            if isinstance(message, AIMessage):
                last_message = message
                break
        else:
            last_message = messages[-1]
        
        content = last_message.content.lower()
        
        # Check for approval signals
        if any(signal in content for signal in ["approved", "plan approved", "proceeding with implementation"]):
            return "approved"
        elif any(signal in content for signal in ["rejected", "plan rejected", "need revision"]):
            return "rejected"
        elif any(signal in content for signal in ["plan complete", "implementation ready"]):
            return "approved"
        else:
            return "continue"
    
    def _software_engineer_router(self, state) -> Literal["continue", "analyze_code", "edit_file", "tools", "__end__"]:
        """Route from Software Engineer based on message content following reference pattern."""
        messages = state["messages"]
        
        # Find the last AI message
        for message in reversed(messages):
            if isinstance(message, AIMessage):
                last_ai_message = message
                break
        else:
            last_ai_message = messages[-1]
        
        # Check for tool calls first
        if last_ai_message.tool_calls:
            return "tools"
        
        # Check for specific routing keywords (following reference pattern)
        content = last_ai_message.content
        if "ANALYZE CODE" in content:
            return "analyze_code"
        if "EDIT FILE" in content:
            return "edit_file"
        if "PATCH COMPLETED" in content:
            return "__end__"
        
        # Check consecutive visits to prevent infinite loops
        consecutive_visits = state.get("consecutive_visits", {})
        swe_visits = consecutive_visits.get(self.software_engineer_name, 0)
        
        if swe_visits >= 5:  # Prevent infinite loops
            return "__end__"
        
        return "continue"
    
    def _code_analyzer_router(self, state) -> Literal["continue", "done", "edit_file", "tools"]:
        """Route from Code Analyzer based on message content following reference pattern."""
        messages = state["messages"]
        
        # Find the last AI message
        for message in reversed(messages):
            if isinstance(message, AIMessage):
                last_ai_message = message
                break
        else:
            last_ai_message = messages[-1]
        
        # Check for tool calls first
        if last_ai_message.tool_calls:
            return "tools"
        
        # Check for specific routing keywords (following reference pattern)
        content = last_ai_message.content
        if "ANALYSIS COMPLETE" in content:
            return "done"
        if "EDIT FILE" in content:
            return "edit_file"
        
        # Check consecutive visits to prevent infinite loops
        consecutive_visits = state.get("consecutive_visits", {})
        analyzer_visits = consecutive_visits.get(self.code_analyzer_name, 0)
        
        if analyzer_visits >= 5:  # Prevent infinite loops
            return "done"
        
        return "continue"
    
    def _editor_router(self, state) -> Literal["continue", "done", "tools"]:
        """Route from Editor based on message content following reference pattern."""
        messages = state["messages"]
        
        # Find the last AI message
        for message in reversed(messages):
            if isinstance(message, AIMessage):
                last_ai_message = message
                break
        else:
            last_ai_message = messages[-1]
        
        # Check for tool calls first
        if last_ai_message.tool_calls:
            return "tools"
        
        # Check for specific routing keywords (following reference pattern)
        content = last_ai_message.content
        if "EDITING COMPLETED" in content:
            return "done"
        
        # Check consecutive visits to prevent infinite loops
        consecutive_visits = state.get("consecutive_visits", {})
        editor_visits = consecutive_visits.get(self.editor_name, 0)
        
        if editor_visits >= 5:  # Prevent infinite loops
            return "done"
        
        return "continue"
    

    
    def run_workflow(self, task_description: str) -> Dict[str, Any]:
        """Run the clean workflow."""
        logger.info(f"🚀 Starting clean SWE workflow with task: {task_description}")
        
        # Create initial state
        initial_state = create_initial_state(task_description)
        initial_state["messages"] = [HumanMessage(content=task_description)]
        
        # Compile and run workflow
        try:
            app = self.workflow.compile()
            config = {"recursion_limit": 50}  # Increased limit
            final_state = app.invoke(initial_state, config=config)
            
            return {
                "task_description": task_description,
                "final_state": final_state,
                "message_count": len(final_state["messages"]),
                "final_sender": final_state["sender"],
                "success": True
            }
            
        except Exception as e:
            logger.error(f"Clean workflow execution failed: {e}")
            return {
                "task_description": task_description,
                "error": str(e),
                "success": False
            }