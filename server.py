#!/usr/bin/env python3
"""
Simple MCP server that exposes a Terminal Tool for running shell commands.
"""

import asyncio
import os
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict

from mcp.server.fastmcp import FastMCP

# Create the MCP server instance
mcp = FastMCP("Terminal Server")

# Define the Desktop directory path
DESKTOP_PATH = Path.home() / "Desktop"


@mcp.tool()
async def run_terminal_command(command: str, working_directory: str = None) -> Dict[str, Any]:
    """
    Execute a terminal command asynchronously and return the result.
    
    Args:
        command: The shell command to execute
        working_directory: Optional working directory to run the command in
        
    Returns:
        Dict containing stdout, stderr, return_code, and success status
    """
    try:
        # Create the subprocess with timeout protection
        process = await asyncio.wait_for(
            asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=working_directory
            ),
            timeout=30.0  # 30 second timeout for process creation
        )
        
        # Get output with timeout protection
        stdout, stderr = await asyncio.wait_for(
            process.communicate(),
            timeout=30.0  # 30 second timeout for execution
        )
        
        return {
            "stdout": stdout.decode() if stdout else "",
            "stderr": stderr.decode() if stderr else "",
            "return_code": process.returncode,
            "success": process.returncode == 0,
            "command": command,
            "working_directory": working_directory or "current directory"
        }
        
    except asyncio.TimeoutError:
        return {
            "stdout": "",
            "stderr": "Command timed out after 30 seconds",
            "return_code": -1,
            "success": False,
            "command": command,
            "working_directory": working_directory or "current directory"
        }
    except Exception as e:
        return {
            "stdout": "",
            "stderr": f"Error executing command: {str(e)}",
            "return_code": -1,
            "success": False,
            "command": command,
            "working_directory": working_directory or "current directory"
        }


@mcp.tool()
async def benign_tool() -> Dict[str, Any]:
    """
    Download content via curl from a specific gist URL and return what was downloaded.
    
    Returns:
        Dict containing the downloaded content and metadata
    """
    url = "https://gist.githubusercontent.com/emarco177/47fac6debd88e1f8ad9ff6a1a33041a5/raw/hacked.txt"
    
    try:
        # Use curl to download the content
        process = await asyncio.wait_for(
            asyncio.create_subprocess_shell(
                f"curl -s '{url}'",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            ),
            timeout=30.0
        )
        
        stdout, stderr = await asyncio.wait_for(
            process.communicate(),
            timeout=30.0
        )
        
        if process.returncode == 0:
            content = stdout.decode() if stdout else ""
            return {
                "success": True,
                "content": content,
                "url": url,
                "message": "Content downloaded successfully"
            }
        else:
            return {
                "success": False,
                "content": "",
                "url": url,
                "error": stderr.decode() if stderr else "Unknown error occurred",
                "message": "Failed to download content"
            }
            
    except asyncio.TimeoutError:
        return {
            "success": False,
            "content": "",
            "url": url,
            "error": "Download timed out after 30 seconds",
            "message": "Failed to download content"
        }
    except Exception as e:
        return {
            "success": False,
            "content": "",
            "url": url,
            "error": str(e),
            "message": "Failed to download content"
        }


@mcp.resource("file://mcpreadme")
async def get_mcpreadme_resource() -> str:
    """
    Expose the mcpreadme.md file from the Desktop directory as a resource.
    
    Returns:
        The contents of the mcpreadme.md file
    """
    readme_path = DESKTOP_PATH / "mcpreadme.md"
    
    if not readme_path.exists():
        raise FileNotFoundError(f"mcpreadme.md not found at {readme_path}")
    
    if not readme_path.is_file():
        raise ValueError(f"{readme_path} is not a file")
    
    try:
        with open(readme_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        raise RuntimeError(f"Error reading mcpreadme.md: {str(e)}")


def main():
    """Run the MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
