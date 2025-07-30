# SWE Agent SDK Examples

This directory contains examples for integrating the SWE Agent into various IDEs and external tools.

## Available Examples

### 1. Sublime Text Plugin (`sublime_plugin.py`)

A comprehensive Sublime Text plugin that provides:
- Custom task execution via Command Palette
- Code fixing at cursor position
- Code analysis for entire files
- Right-click context menu integration
- Status monitoring

**Installation:**
1. Copy `sublime_plugin.py` to your Sublime Text `Packages/User` directory
2. Install the SWE Agent SDK: `pip install swe-agent-sdk`
3. Restart Sublime Text

**Usage:**
- `Ctrl+Shift+P` → "SWE Agent: Execute Task"
- Right-click → "SWE Agent: Fix This"
- Command Palette → "SWE Agent: Analyze Code"

### 2. VS Code Extension (`vscode_extension.js`)

A VS Code extension with full SWE Agent integration:
- Task execution with progress tracking
- Code fixing and analysis
- Status bar integration
- Context menu commands
- Configurable settings

**Installation:**
1. Create a new VS Code extension project
2. Copy `vscode_extension.js` and `package.json` to your project
3. Copy the `scripts/` directory to your project
4. Install the SWE Agent SDK: `pip install swe-agent-sdk`
5. Package and install the extension

**Usage:**
- `Ctrl+Shift+S` → Execute custom task
- `Ctrl+Shift+F` → Fix code at cursor
- `Ctrl+Shift+A` → Analyze current file
- Status bar item shows agent status

### 3. Helper Scripts (`scripts/`)

Python scripts that bridge VS Code extension with SWE Agent:
- `execute_task.py` - Execute tasks and return JSON results
- `get_status.py` - Get agent status information

## SDK Features

The SWE Agent SDK provides:

### Core Classes
- `SWEAgentClient` - Main client for interacting with the agent
- `TaskRequest` - Request object for task execution
- `TaskResponse` - Response object with results and metadata
- `AgentStatus` - System status information
- `FileContext` - File-specific context and metadata
- `GitStatus` - Git repository status

### Key Features
- **Synchronous and Asynchronous Execution** - Execute tasks immediately or in background
- **Context Management** - Automatically handle file context and working directories
- **Git Integration** - Real-time git status and change tracking
- **Language Detection** - Automatic programming language detection
- **Error Handling** - Comprehensive exception handling with specific error types
- **Progress Tracking** - Monitor task execution and agent activity
- **Tool Usage Analytics** - Track which tools are being used by agents

### Example Usage

```python
from sdk import SWEAgentClient, TaskRequest

# Create client
client = SWEAgentClient(
    working_directory="/path/to/project",
    log_level="INFO",
    timeout=300
)

# Create task request
request = TaskRequest(
    task="Create a Python class for user authentication",
    context_files=["auth.py", "models.py"],
    use_planner=True
)

# Execute task
response = client.execute_task(request)

if response.status == TaskStatus.COMPLETED:
    print(f"Task completed: {response.result}")
    print(f"Files modified: {response.files_modified}")
else:
    print(f"Task failed: {response.error}")
```

## Configuration

### Sublime Text
Configure the plugin by editing your Sublime Text user settings:

```json
{
    "swe_agent": {
        "sdk_path": "/path/to/swe-agent-sdk",
        "python_path": "python",
        "timeout": 300,
        "log_level": "INFO"
    }
}
```

### VS Code
Configure the extension through VS Code settings:

```json
{
    "swe-agent.pythonPath": "python",
    "swe-agent.sdkPath": "/path/to/swe-agent-sdk",
    "swe-agent.timeout": 300,
    "swe-agent.usePlanner": false,
    "swe-agent.logLevel": "INFO"
}
```

## Error Handling

The SDK provides specific exception types for different error scenarios:

- `TaskExecutionException` - Task execution failures
- `ConnectionException` - Connection issues
- `ValidationException` - Input validation errors
- `TimeoutException` - Task timeout errors
- `AgentNotAvailableException` - Agent availability issues

## Support

For issues and questions:
1. Check the SDK documentation
2. Review the example implementations
3. Test with the standalone SWE Agent CLI first
4. Report issues with detailed error messages and logs