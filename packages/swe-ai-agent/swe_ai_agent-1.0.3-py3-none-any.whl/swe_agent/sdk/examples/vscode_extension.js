/**
 * VS Code Extension Example for SWE Agent Integration
 * 
 * This example demonstrates how to create a VS Code extension that
 * integrates with the SWE Agent using the Python SDK.
 * 
 * Installation:
 * 1. Create a new VS Code extension project
 * 2. Copy this code into your extension.js
 * 3. Install the SWE Agent SDK in your system Python
 * 4. Configure the extension settings
 */

const vscode = require('vscode');
const { spawn } = require('child_process');
const path = require('path');

/**
 * Activate the extension
 */
function activate(context) {
    console.log('SWE Agent extension is now active');

    // Register commands
    const executeTaskCommand = vscode.commands.registerCommand('swe-agent.executeTask', executeTask);
    const fixCodeCommand = vscode.commands.registerCommand('swe-agent.fixCode', fixCode);
    const analyzeCodeCommand = vscode.commands.registerCommand('swe-agent.analyzeCode', analyzeCode);
    const showStatusCommand = vscode.commands.registerCommand('swe-agent.showStatus', showStatus);

    // Register context menu items
    const fixThisCommand = vscode.commands.registerCommand('swe-agent.fixThis', fixThis);

    // Add to context subscriptions
    context.subscriptions.push(
        executeTaskCommand,
        fixCodeCommand,
        analyzeCodeCommand,
        showStatusCommand,
        fixThisCommand
    );

    // Register status bar item
    const statusBarItem = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Right, 100);
    statusBarItem.text = "$(tools) SWE Agent";
    statusBarItem.command = 'swe-agent.showStatus';
    statusBarItem.tooltip = 'Click to show SWE Agent status';
    statusBarItem.show();
    context.subscriptions.push(statusBarItem);
}

/**
 * Execute a custom task
 */
async function executeTask() {
    try {
        const task = await vscode.window.showInputBox({
            prompt: 'Enter task description',
            placeHolder: 'e.g., "Create a Python calculator class"'
        });

        if (!task) {
            return;
        }

        const activeEditor = vscode.window.activeTextEditor;
        const workspaceFolder = vscode.workspace.workspaceFolders?.[0];
        
        if (!workspaceFolder) {
            vscode.window.showErrorMessage('Please open a workspace folder');
            return;
        }

        const contextFiles = activeEditor ? [activeEditor.document.uri.fsPath] : [];
        const workingDirectory = workspaceFolder.uri.fsPath;

        await executeSWEAgent(task, contextFiles, workingDirectory);

    } catch (error) {
        vscode.window.showErrorMessage(`Error executing task: ${error.message}`);
    }
}

/**
 * Fix code at cursor position
 */
async function fixCode() {
    const activeEditor = vscode.window.activeTextEditor;
    if (!activeEditor) {
        vscode.window.showErrorMessage('No active editor');
        return;
    }

    const document = activeEditor.document;
    const selection = activeEditor.selection;
    
    let codeText;
    let lineNumber;
    
    if (selection.isEmpty) {
        // Use current line
        const line = document.lineAt(selection.active.line);
        codeText = line.text;
        lineNumber = line.lineNumber + 1;
    } else {
        // Use selection
        codeText = document.getText(selection);
        lineNumber = selection.start.line + 1;
    }

    const fileName = path.basename(document.uri.fsPath);
    const task = `Fix the following code issue in ${fileName} at line ${lineNumber}:\n\n${codeText}`;

    const workspaceFolder = vscode.workspace.workspaceFolders?.[0];
    if (!workspaceFolder) {
        vscode.window.showErrorMessage('Please open a workspace folder');
        return;
    }

    await executeSWEAgent(task, [document.uri.fsPath], workspaceFolder.uri.fsPath);
}

/**
 * Analyze current file
 */
async function analyzeCode() {
    const activeEditor = vscode.window.activeTextEditor;
    if (!activeEditor) {
        vscode.window.showErrorMessage('No active editor');
        return;
    }

    const document = activeEditor.document;
    const fileName = path.basename(document.uri.fsPath);
    const task = `Analyze the code in ${fileName} and provide insights on code quality, structure, potential issues, and improvement suggestions`;

    const workspaceFolder = vscode.workspace.workspaceFolders?.[0];
    if (!workspaceFolder) {
        vscode.window.showErrorMessage('Please open a workspace folder');
        return;
    }

    await executeSWEAgent(task, [document.uri.fsPath], workspaceFolder.uri.fsPath);
}

/**
 * Fix code at cursor (context menu)
 */
async function fixThis() {
    await fixCode();
}

/**
 * Show SWE Agent status
 */
async function showStatus() {
    try {
        const result = await runPythonScript('get_status.py', []);
        
        if (result.success) {
            const status = JSON.parse(result.output);
            
            const statusText = `SWE Agent Status
===============
Running: ${status.is_running}
Uptime: ${status.uptime.toFixed(2)}s
Total Tasks: ${status.total_tasks}
Successful: ${status.successful_tasks}
Failed: ${status.failed_tasks}
Available Agents: ${status.agents_available.join(', ')}`;

            vscode.window.showInformationMessage(statusText);
        } else {
            vscode.window.showErrorMessage(`Error getting status: ${result.error}`);
        }
    } catch (error) {
        vscode.window.showErrorMessage(`Error: ${error.message}`);
    }
}

/**
 * Execute SWE Agent task
 */
async function executeSWEAgent(task, contextFiles, workingDirectory) {
    return vscode.window.withProgress({
        location: vscode.ProgressLocation.Notification,
        title: "SWE Agent",
        cancellable: true
    }, async (progress, token) => {
        progress.report({ increment: 0, message: "Starting task..." });

        try {
            const scriptArgs = [
                '--task', task,
                '--working-directory', workingDirectory,
                '--context-files', contextFiles.join(',')
            ];

            const result = await runPythonScript('execute_task.py', scriptArgs, token);
            
            if (result.success) {
                progress.report({ increment: 100, message: "Task completed successfully" });
                
                const response = JSON.parse(result.output);
                await showTaskResult(response);
                
                // Refresh file if it was modified
                if (response.files_modified && response.files_modified.length > 0) {
                    for (const filePath of response.files_modified) {
                        const document = await vscode.workspace.openTextDocument(filePath);
                        await vscode.window.showTextDocument(document);
                    }
                }
            } else {
                progress.report({ increment: 100, message: "Task failed" });
                vscode.window.showErrorMessage(`Task failed: ${result.error}`);
            }
        } catch (error) {
            progress.report({ increment: 100, message: "Task failed" });
            vscode.window.showErrorMessage(`Error: ${error.message}`);
        }
    });
}

/**
 * Run Python script with SWE Agent SDK
 */
function runPythonScript(scriptName, args, cancellationToken = null) {
    return new Promise((resolve, reject) => {
        const config = vscode.workspace.getConfiguration('swe-agent');
        const pythonPath = config.get('pythonPath', 'python');
        const sdkPath = config.get('sdkPath', '');
        
        const scriptPath = path.join(__dirname, 'scripts', scriptName);
        const pythonArgs = [scriptPath, ...args];
        
        const env = { ...process.env };
        if (sdkPath) {
            env.PYTHONPATH = sdkPath;
        }
        
        const pythonProcess = spawn(pythonPath, pythonArgs, {
            cwd: vscode.workspace.workspaceFolders?.[0]?.uri.fsPath,
            env: env
        });
        
        let stdout = '';
        let stderr = '';
        
        pythonProcess.stdout.on('data', (data) => {
            stdout += data.toString();
        });
        
        pythonProcess.stderr.on('data', (data) => {
            stderr += data.toString();
        });
        
        pythonProcess.on('close', (code) => {
            if (code === 0) {
                resolve({ success: true, output: stdout });
            } else {
                resolve({ success: false, error: stderr || 'Unknown error' });
            }
        });
        
        pythonProcess.on('error', (error) => {
            reject(error);
        });
        
        // Handle cancellation
        if (cancellationToken) {
            cancellationToken.onCancellationRequested(() => {
                pythonProcess.kill();
                reject(new Error('Task cancelled'));
            });
        }
    });
}

/**
 * Show task result in a new document
 */
async function showTaskResult(response) {
    const resultContent = `SWE Agent Task Result
====================
Task ID: ${response.task_id}
Status: ${response.status}
Execution Time: ${response.execution_time.toFixed(2)}s
Timestamp: ${response.timestamp}

Result:
${response.result || 'No result content'}

Tools Used:
${response.tools_used.join(', ') || 'None'}

Files Modified:
${response.files_modified.join(', ') || 'None'}

Agent Visits:
${JSON.stringify(response.agent_visits, null, 2)}
`;

    const document = await vscode.workspace.openTextDocument({
        content: resultContent,
        language: 'markdown'
    });
    
    await vscode.window.showTextDocument(document);
}

/**
 * Deactivate the extension
 */
function deactivate() {}

module.exports = {
    activate,
    deactivate
};