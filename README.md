# Shell Server MCP

A simple Model Context Protocol (MCP) server that provides terminal command execution capabilities.

## Features

- **Async Terminal Tool**: Execute shell commands asynchronously with timeout protection
- **Working Directory Support**: Run commands in specific directories
- **Comprehensive Output**: Returns stdout, stderr, return codes, and success status
- **Error Handling**: Graceful handling of timeouts and execution errors
- **Non-blocking Execution**: Async implementation allows for better concurrency

## Installation

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -e .
   ```

## Usage

### Running the Server

```bash
python server.py
```

The server will start and listen for MCP protocol messages on stdin/stdout.

### Available Tools

#### `run_terminal_command`

Execute a shell command asynchronously and return detailed results.

**Parameters:**
- `command` (string, required): The shell command to execute
- `working_directory` (string, optional): Directory to run the command in

**Returns:**
- `stdout`: Command output
- `stderr`: Error output  
- `return_code`: Exit code of the command
- `success`: Boolean indicating if command succeeded (return_code == 0)
- `command`: The executed command
- `working_directory`: Directory where command was executed

**Example:**
```json
{
  "command": "ls -la",
  "working_directory": "/home/user"
}
```

## Security Features

- **Timeout Protection**: Commands are automatically terminated after 30 seconds
- **Error Isolation**: Exceptions are caught and returned as structured error responses
- **No Privilege Escalation**: Runs with the same permissions as the server process

## Development

The server is built using FastMCP, which provides a simple decorator-based approach to creating MCP tools. The terminal command execution is implemented asynchronously using `asyncio` for better performance and non-blocking behavior.

## License

MIT License
