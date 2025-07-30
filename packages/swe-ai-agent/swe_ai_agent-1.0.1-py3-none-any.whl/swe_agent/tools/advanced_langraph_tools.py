"""
Advanced LangGraph Tool Wrappers with Shell, Git, and Enhanced Code Analysis
Integrates the uploaded tools into LangGraph callable functions.
"""

import logging
import os
import subprocess
import json
from typing import Dict, Any, List, Optional
from pathlib import Path
from langchain.tools import tool
from ..tools.file_operations import FileOperations
from ..tools.code_analysis import CodeAnalyzer
from ..tools.shell_operations import ShellOperations, GitOperations, WorkspaceManager, AdvancedCodeSearch
from ..tools.tool_usage_tracker import get_tool_tracker

logger = logging.getLogger(__name__)

class AdvancedLangGraphTools:
    """
    Advanced wrapper class that includes shell execution, git operations,
    and enhanced code analysis capabilities.
    """
    
    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)
        self.file_ops = FileOperations(repo_path)
        self.code_analyzer = CodeAnalyzer(repo_path)
        self.shell_ops = ShellOperations(repo_path)
        self.git_ops = GitOperations(repo_path)
        self.workspace_manager = WorkspaceManager(repo_path)
        self.code_search = AdvancedCodeSearch(repo_path)
        self._create_tools()
    
    def _create_tools(self):
        """Create advanced LangGraph tools."""
        file_ops = self.file_ops
        code_analyzer = self.code_analyzer
        shell_ops = self.shell_ops
        git_ops = self.git_ops
        workspace_manager = self.workspace_manager
        code_search = self.code_search
        repo_path = self.repo_path
        
        # Basic file operations (existing)
        @tool
        def create_file(filename: str, content: str) -> str:
            """Create a new file with the given content."""
            tracker = get_tool_tracker()
            call_id = tracker.start_tool_call("advanced_tools", "create_file", {"filename": filename})
            
            try:
                result = file_ops.create_file(filename, content)
                success = result["success"]
                response = f"✅ Successfully created file: {filename}" if success else f"❌ Failed to create file: {result.get('error', 'Unknown error')}"
                
                tracker.end_tool_call(call_id, "advanced_tools", "create_file", success, 
                                    result.get('error') if not success else None, 
                                    f"Created {filename}" if success else None)
                return response
            except Exception as e:
                tracker.end_tool_call(call_id, "advanced_tools", "create_file", False, str(e))
                raise
        
        @tool
        def open_file(filename: str, line_number: int = 0, window_size: int = 50) -> str:
            """
            Open and read a file's content with smart defaults.
            
            Args:
                filename: Path to the file to open
                line_number: Starting line number (0 for beginning)
                window_size: Number of lines to read (50 default, -1 for entire file)
                
            Returns:
                File content with line numbers for easy reference
            """
            tracker = get_tool_tracker()
            call_id = tracker.start_tool_call("advanced_tools", "open_file", {"filename": filename, "line_number": line_number, "window_size": window_size})
            
            try:
                result = file_ops.open_file(filename, line_number, window_size)
                if result["success"]:
                    response = f"📄 File: {filename}\n{result['lines']}"
                    tracker.end_tool_call(call_id, "advanced_tools", "open_file", True, None, f"Opened {filename}")
                    return response
                else:
                    error_msg = result.get('error', 'Unknown error')
                    response = f"❌ Failed to open file: {error_msg}"
                    tracker.end_tool_call(call_id, "advanced_tools", "open_file", False, error_msg)
                    return response
            except Exception as e:
                tracker.end_tool_call(call_id, "advanced_tools", "open_file", False, str(e))
                raise
        
        @tool
        def edit_file(filename: str, new_content: str, line_number: int, num_lines: int = 1) -> str:
            """
            Edit a file by replacing content at specific lines.
            
            Args:
                filename: Path to the file to edit
                new_content: New content to insert
                line_number: Line number to start editing (1-based)
                num_lines: Number of lines to replace (default: 1)
                
            Returns:
                Success or error message
                
            Note: Consider using replace_in_file or rewrite_file for easier editing
            """
            tracker = get_tool_tracker()
            call_id = tracker.start_tool_call("advanced_tools", "edit_file", {"filename": filename, "line_number": line_number, "num_lines": num_lines})
            
            try:
                result = file_ops.edit_file(filename, new_content, line_number, num_lines)
                if result["success"]:
                    response = f"✅ Successfully edited file: {filename}"
                    tracker.end_tool_call(call_id, "advanced_tools", "edit_file", True, None, f"Edited {filename}")
                    return response
                else:
                    error_msg = result.get('error', 'Unknown error')
                    response = f"❌ Failed to edit file: {error_msg}"
                    tracker.end_tool_call(call_id, "advanced_tools", "edit_file", False, error_msg)
                    return response
            except Exception as e:
                tracker.end_tool_call(call_id, "advanced_tools", "edit_file", False, str(e))
                raise
        
        @tool
        def replace_in_file(filename: str, old_text: str, new_text: str, max_replacements: int = -1) -> str:
            """Replace text in a file using find and replace."""
            tracker = get_tool_tracker()
            call_id = tracker.start_tool_call("advanced_tools", "replace_in_file", {"filename": filename, "old_text": old_text, "new_text": new_text})
            
            try:
                target_path = repo_path / filename
                if not target_path.exists():
                    response = f"❌ File not found: {filename}"
                    tracker.end_tool_call(call_id, "advanced_tools", "replace_in_file", False, f"File not found: {filename}")
                    return response
                
                # Read file content
                with open(target_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Perform replacement
                if max_replacements == -1:
                    new_content = content.replace(old_text, new_text)
                    replacements = content.count(old_text)
                else:
                    new_content = content.replace(old_text, new_text, max_replacements)
                    replacements = min(content.count(old_text), max_replacements)
                
                if replacements == 0:
                    response = f"❌ Text '{old_text}' not found in {filename}"
                    tracker.end_tool_call(call_id, "advanced_tools", "replace_in_file", False, f"Text not found: {old_text}")
                    return response
                
                # Write back to file
                with open(target_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                response = f"✅ Successfully replaced {replacements} occurrence(s) of '{old_text}' with '{new_text}' in {filename}"
                tracker.end_tool_call(call_id, "advanced_tools", "replace_in_file", True, None, f"Replaced {replacements} occurrences in {filename}")
                return response
            except Exception as e:
                tracker.end_tool_call(call_id, "advanced_tools", "replace_in_file", False, str(e))
                raise
        
        @tool
        def rewrite_file(filename: str, new_content: str) -> str:
            """Completely rewrite a file with new content."""
            tracker = get_tool_tracker()
            call_id = tracker.start_tool_call("advanced_tools", "rewrite_file", {"filename": filename})
            
            try:
                target_path = repo_path / filename
                
                # Create backup if file exists
                if target_path.exists():
                    backup_path = target_path.with_suffix(target_path.suffix + '.backup')
                    backup_path.write_text(target_path.read_text())
                
                # Write new content
                with open(target_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                response = f"✅ Successfully rewrote file: {filename}"
                tracker.end_tool_call(call_id, "advanced_tools", "rewrite_file", True, None, f"Rewrote {filename}")
                return response
            except Exception as e:
                tracker.end_tool_call(call_id, "advanced_tools", "rewrite_file", False, str(e))
                raise
        
        @tool
        def list_files(directory: str = ".") -> str:
            """
            List files and directories in the specified directory.
            
            Args:
                directory: Directory path to list (default: current directory)
                
            Returns:
                Formatted list of files and directories with clear separation
            """
            tracker = get_tool_tracker()
            call_id = tracker.start_tool_call("advanced_tools", "list_files", {"directory": directory})
            
            try:
                result = file_ops.list_files(directory)
                if result["success"]:
                    files = result["files"]
                    if files and isinstance(files[0], dict):
                        files_str = "\n".join([f.get('name', str(f)) for f in files[:20]])
                    else:
                        files_str = "\n".join(files[:20])
                    
                    dirs = result["directories"]
                    if dirs and isinstance(dirs[0], dict):
                        dirs_str = "\n".join([d.get('name', str(d)) for d in dirs[:10]])
                    else:
                        dirs_str = "\n".join(dirs[:10])
                    
                    response = f"📁 Files:\n{files_str}\n\n📂 Directories:\n{dirs_str}"
                    tracker.end_tool_call(call_id, "advanced_tools", "list_files", True, None, f"Listed {directory}")
                    return response
                else:
                    error_msg = result.get('error', 'Unknown error')
                    response = f"❌ Failed to list files: {error_msg}"
                    tracker.end_tool_call(call_id, "advanced_tools", "list_files", False, error_msg)
                    return response
            except Exception as e:
                tracker.end_tool_call(call_id, "advanced_tools", "list_files", False, str(e))
                raise
        
        # Shell execution capabilities
        @tool
        def execute_shell_command(command: str, timeout: int = 30) -> str:
            """
            Execute a shell command with timeout.
            
            Args:
                command: Shell command to execute
                timeout: Timeout in seconds (default: 30)
                
            Returns:
                Command output and status
            """
            tracker = get_tool_tracker()
            call_id = tracker.start_tool_call("advanced_tools", "execute_shell_command", {"command": command, "timeout": timeout})
            
            try:
                result = shell_ops.execute_command(command, timeout)
                success = result['success']
                response = f"✅ Command executed successfully:\n{result['stdout']}" if success else f"❌ Command failed (exit code {result['exit_code']}):\n{result['stderr']}"
                
                tracker.end_tool_call(call_id, "advanced_tools", "execute_shell_command", success,
                                    result['stderr'] if not success else None,
                                    f"Executed: {command}" if success else None)
                return response
            except Exception as e:
                tracker.end_tool_call(call_id, "advanced_tools", "execute_shell_command", False, str(e))
                raise
        
        @tool
        def get_command_history() -> str:
            """
            Get the history of executed shell commands.
            
            Returns:
                Formatted list of recently executed commands with execution order
            """
            tracker = get_tool_tracker()
            call_id = tracker.start_tool_call("advanced_tools", "get_command_history", {})
            
            try:
                history = shell_ops.get_command_history()
                if not history:
                    response = "📜 No commands executed yet"
                else:
                    history_str = "\n".join([f"{i+1}. {cmd['command']}" for i, cmd in enumerate(history)])
                    response = f"📜 Recent command history:\n{history_str}"
                
                tracker.end_tool_call(call_id, "advanced_tools", "get_command_history", True, None, f"Retrieved {len(history)} commands")
                return response
            except Exception as e:
                tracker.end_tool_call(call_id, "advanced_tools", "get_command_history", False, str(e))
                raise
        
        # Git operations
        @tool
        def git_status() -> str:
            """
            Get git repository status showing changes, staged files, and branch info.
            
            Returns:
                Git status information including modified files and staging area
            """
            tracker = get_tool_tracker()
            call_id = tracker.start_tool_call("advanced_tools", "git_status", {})
            
            try:
                result = git_ops.git_status()
                if result['success']:
                    if result['stdout'].strip():
                        response = f"🔄 Git status:\n{result['stdout']}"
                    else:
                        response = "✅ Working directory clean"
                    tracker.end_tool_call(call_id, "advanced_tools", "git_status", True, None, "Retrieved git status")
                    return response
                else:
                    error_msg = result['stderr']
                    response = f"❌ Git status failed: {error_msg}"
                    tracker.end_tool_call(call_id, "advanced_tools", "git_status", False, error_msg)
                    return response
            except Exception as e:
                tracker.end_tool_call(call_id, "advanced_tools", "git_status", False, str(e))
                raise
        
        @tool
        def git_diff(file_path: str = None) -> str:
            """
            Get git diff for changes.
            
            Args:
                file_path: Specific file to diff (optional)
                
            Returns:
                Git diff output
            """
            result = git_ops.git_diff(file_path)
            if result['success']:
                if result['stdout'].strip():
                    return f"📝 Git diff:\n{result['stdout']}"
                else:
                    return "✅ No changes to show"
            else:
                return f"❌ Git diff failed: {result['stderr']}"
        
        @tool
        def git_add(file_path: str) -> str:
            """
            Add file to git staging area.
            
            Args:
                file_path: Path to file to add
                
            Returns:
                Git add result
            """
            result = git_ops.git_add(file_path)
            if result['success']:
                return f"✅ Added {file_path} to git staging area"
            else:
                return f"❌ Git add failed: {result['stderr']}"
        
        @tool
        def git_commit(message: str) -> str:
            """
            Commit staged changes.
            
            Args:
                message: Commit message
                
            Returns:
                Git commit result
            """
            result = git_ops.git_commit(message)
            if result['success']:
                return f"✅ Committed changes: {message}"
            else:
                return f"❌ Git commit failed: {result['stderr']}"
        
        # Enhanced code analysis
        @tool
        def analyze_file_advanced(filename: str) -> str:
            """
            Advanced file analysis with detailed structure information.
            
            Args:
                filename: Path to the file to analyze
                
            Returns:
                Comprehensive analysis including language, structure, and components
            """
            tracker = get_tool_tracker()
            call_id = tracker.start_tool_call("advanced_tools", "analyze_file_advanced", {"filename": filename})
            
            try:
                result = code_analyzer.analyze_file(filename)
                if result["success"]:
                    response = f"""🔍 Advanced Analysis: {filename}

Language: {result['language']}
Lines: {result['line_count']}
Functions: {len(result['functions'])}
Classes: {len(result['classes'])}
Imports: {len(result['imports'])}

🔧 Functions:
{chr(10).join([f"  - {f['name']} (line {f['line_start']})" for f in result['functions'][:10]])}

📋 Classes:
{chr(10).join([f"  - {c['name']} (lines {c['line_start']}-{c['line_end']})" for c in result['classes'][:10]])}

📦 Imports:
{chr(10).join([f"  - {imp}" for imp in result['imports'][:10]])}"""
                    tracker.end_tool_call(call_id, "advanced_tools", "analyze_file_advanced", True, None, f"Analyzed {filename}")
                    return response
                else:
                    error_msg = result.get('error', 'Unknown error')
                    response = f"❌ Analysis failed: {error_msg}"
                    tracker.end_tool_call(call_id, "advanced_tools", "analyze_file_advanced", False, error_msg)
                    return response
            except Exception as e:
                tracker.end_tool_call(call_id, "advanced_tools", "analyze_file_advanced", False, str(e))
                raise
        
        @tool
        def search_code_semantic(query: str, file_pattern: str = "*.py") -> str:
            """
            Semantic code search using pattern matching across files.
            
            Args:
                query: Search query (can be function names, class names, or code patterns)
                file_pattern: File pattern to search in (default: *.py for Python files)
                
            Returns:
                Search results with file paths and line numbers
                
            Examples:
                - search_code_semantic("def create_file") - finds function definitions
                - search_code_semantic("class Agent", "*.py") - finds class definitions
                - search_code_semantic("import langchain", "*") - finds imports
            """
            tracker = get_tool_tracker()
            call_id = tracker.start_tool_call("advanced_tools", "search_code_semantic", {"query": query, "file_pattern": file_pattern})
            
            try:
                result = code_search.search_code(query, file_pattern)
                if result['success']:
                    if result['stdout'].strip():
                        response = f"🔍 Found matches for '{query}':\n{result['stdout']}"
                        tracker.end_tool_call(call_id, "advanced_tools", "search_code_semantic", True, None, f"Found matches for '{query}'")
                    else:
                        response = f"🔍 No matches found for '{query}'"
                        tracker.end_tool_call(call_id, "advanced_tools", "search_code_semantic", True, None, f"No matches for '{query}'")
                    return response
                else:
                    error_msg = result['stderr']
                    response = f"❌ Search error: {error_msg}"
                    tracker.end_tool_call(call_id, "advanced_tools", "search_code_semantic", False, error_msg)
                    return response
            except Exception as e:
                tracker.end_tool_call(call_id, "advanced_tools", "search_code_semantic", False, str(e))
                raise
        
        @tool
        def get_workspace_info() -> str:
            """
            Get comprehensive workspace information including files, directories, and project structure.
            
            Returns:
                Detailed workspace overview with file counts, types, and recent files
            """
            tracker = get_tool_tracker()
            call_id = tracker.start_tool_call("advanced_tools", "get_workspace_info", {})
            
            try:
                result = workspace_manager.get_workspace_info()
                if result['success']:
                    info = result['workspace_info']
                    branch_result = git_ops.git_branch()
                    branch = branch_result['stdout'].strip() if branch_result['success'] else 'Not a git repository'
                    
                    response = f"""🏢 Workspace Information:

📁 Repository: {info['repository_path']}
🌿 Git Branch: {branch}
📊 Total Files: {len(info['files'])}
📂 Directories: {len(info['directories'])}
💾 Size: {info['size_mb']:.2f} MB

🗂️ File Types:
{chr(10).join([f"  - {ext}: {count}" for ext, count in info['languages'].items()])}

📁 Recent Files:
{chr(10).join([f"  - {f['name']}" for f in info['files'][:10]])}"""
                    tracker.end_tool_call(call_id, "advanced_tools", "get_workspace_info", True, None, "Retrieved workspace info")
                    return response
                else:
                    error_msg = result['error']
                    response = f"❌ Workspace info error: {error_msg}"
                    tracker.end_tool_call(call_id, "advanced_tools", "get_workspace_info", False, error_msg)
                    return response
            except Exception as e:
                tracker.end_tool_call(call_id, "advanced_tools", "get_workspace_info", False, str(e))
                raise
        
        # Advanced code search tools
        @tool
        def find_function_definitions(function_name: str, language: str = "python") -> str:
            """
            Find function definitions across the codebase with file locations.
            
            Args:
                function_name: Name of the function to find (exact match or partial)
                language: Programming language (default: python, also supports: javascript, java, etc.)
                
            Returns:
                Function definition locations with file paths and line numbers
                
            Examples:
                - find_function_definitions("create_file") - finds create_file function
                - find_function_definitions("analyze", "python") - finds analyze functions
            """
            tracker = get_tool_tracker()
            call_id = tracker.start_tool_call("advanced_tools", "find_function_definitions", {"function_name": function_name, "language": language})
            
            try:
                result = code_search.find_function_definitions(function_name, language)
                if result['success']:
                    if result['stdout'].strip():
                        response = f"🔍 Found function definitions for '{function_name}':\n{result['stdout']}"
                        tracker.end_tool_call(call_id, "advanced_tools", "find_function_definitions", True, None, f"Found '{function_name}' functions")
                    else:
                        response = f"🔍 No function definitions found for '{function_name}'"
                        tracker.end_tool_call(call_id, "advanced_tools", "find_function_definitions", True, None, f"No '{function_name}' functions found")
                    return response
                else:
                    error_msg = result['stderr']
                    response = f"❌ Search error: {error_msg}"
                    tracker.end_tool_call(call_id, "advanced_tools", "find_function_definitions", False, error_msg)
                    return response
            except Exception as e:
                tracker.end_tool_call(call_id, "advanced_tools", "find_function_definitions", False, str(e))
                raise
        
        @tool
        def find_class_definitions(class_name: str, language: str = "python") -> str:
            """
            Find class definitions across the codebase with inheritance info.
            
            Args:
                class_name: Name of the class to find (exact match or partial)
                language: Programming language (default: python, also supports: javascript, java, etc.)
                
            Returns:
                Class definition locations with file paths and line numbers
                
            Examples:
                - find_class_definitions("Agent") - finds Agent classes
                - find_class_definitions("Workflow", "python") - finds Workflow classes
            """
            tracker = get_tool_tracker()
            call_id = tracker.start_tool_call("advanced_tools", "find_class_definitions", {"class_name": class_name, "language": language})
            
            try:
                result = code_search.find_class_definitions(class_name, language)
                if result['success']:
                    if result['stdout'].strip():
                        response = f"🔍 Found class definitions for '{class_name}':\n{result['stdout']}"
                        tracker.end_tool_call(call_id, "advanced_tools", "find_class_definitions", True, None, f"Found '{class_name}' classes")
                    else:
                        response = f"🔍 No class definitions found for '{class_name}'"
                        tracker.end_tool_call(call_id, "advanced_tools", "find_class_definitions", True, None, f"No '{class_name}' classes found")
                    return response
                else:
                    error_msg = result['stderr']
                    response = f"❌ Search error: {error_msg}"
                    tracker.end_tool_call(call_id, "advanced_tools", "find_class_definitions", False, error_msg)
                    return response
            except Exception as e:
                tracker.end_tool_call(call_id, "advanced_tools", "find_class_definitions", False, str(e))
                raise
        
        @tool
        def find_imports(module_name: str, language: str = "python") -> str:
            """
            Find import statements across the codebase.
            
            Args:
                module_name: Name of the module to find imports for
                language: Programming language (default: python)
                
            Returns:
                Import statement locations
            """
            result = code_search.find_imports(module_name, language)
            if result['success']:
                if result['stdout'].strip():
                    return f"🔍 Found imports for '{module_name}':\n{result['stdout']}"
                else:
                    return f"🔍 No imports found for '{module_name}'"
            else:
                return f"❌ Search error: {result['stderr']}"
        
        @tool
        def get_directory_tree(max_depth: int = 3) -> str:
            """
            Get directory tree structure.
            
            Args:
                max_depth: Maximum depth to traverse (default: 3)
                
            Returns:
                Directory tree structure
            """
            result = workspace_manager.get_directory_tree(max_depth)
            if result['success']:
                return f"🌳 Directory tree:\n{result['stdout']}"
            else:
                return f"❌ Directory tree error: {result['stderr']}"
        
        @tool
        def search_files_by_name(pattern: str, file_type: str = "*") -> str:
            """
            Search for files by name pattern.
            
            Args:
                pattern: Pattern to search for in file names
                file_type: File type filter (default: all files)
                
            Returns:
                Matching file paths
            """
            result = workspace_manager.search_files(pattern, file_type)
            if result['success']:
                if result['stdout'].strip():
                    return f"🔍 Found files matching '{pattern}':\n{result['stdout']}"
                else:
                    return f"🔍 No files found matching '{pattern}'"
            else:
                return f"❌ File search error: {result['stderr']}"
        
        # Store tools as instance attributes
        self.create_file = create_file
        self.open_file = open_file
        self.edit_file = edit_file
        self.replace_in_file = replace_in_file
        self.rewrite_file = rewrite_file
        self.list_files = list_files
        self.execute_shell_command = execute_shell_command
        self.get_command_history = get_command_history
        self.git_status = git_status
        self.git_diff = git_diff
        self.git_add = git_add
        self.git_commit = git_commit
        self.analyze_file_advanced = analyze_file_advanced
        self.search_code_semantic = search_code_semantic
        self.get_workspace_info = get_workspace_info
        self.find_function_definitions = find_function_definitions
        self.find_class_definitions = find_class_definitions
        self.find_imports = find_imports
        self.get_directory_tree = get_directory_tree
        self.search_files_by_name = search_files_by_name
    
    def get_all_tools(self) -> List:
        """Get all available tools."""
        return [
            self.create_file,
            self.open_file,
            self.edit_file,
            self.replace_in_file,
            self.rewrite_file,
            self.list_files,
            self.execute_shell_command,
            self.get_command_history,
            self.git_status,
            self.git_diff,
            self.git_add,
            self.git_commit,
            self.analyze_file_advanced,
            self.search_code_semantic,
            self.get_workspace_info,
            self.find_function_definitions,
            self.find_class_definitions,
            self.find_imports,
            self.get_directory_tree,
            self.search_files_by_name
        ]