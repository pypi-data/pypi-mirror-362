"""Bash execution tool for LoopLM.

This tool allows the LLM to execute bash commands and capture their output.
"""

import re
import subprocess
from pathlib import Path

from looplm.tools.base import tool

# List of dangerous operations we want to prevent
DANGEROUS_PATTERNS = [
    r"rm\s+-rf\s+[/*]",  # Dangerous rm commands
    r"rm\s+-rf\s+~",  # Remove home directory
    r"rm\s+-rf\s+\$HOME",  # Remove home directory
    r">[>]?\s*/dev/",  # Output redirection to devices
    r"mkfs",  # Format filesystem
    r"dd\s+if=",  # Disk operations
    r";\s*rm\s+-rf",  # Command chain with dangerous rm
    r"&\s*rm\s+-rf",  # Background dangerous rm
    r"curl\s+.*\|\s*sh",  # Pipe curl to shell
    r"wget\s+.*\|\s*sh",  # Pipe wget to shell
    r"sudo\s+rm\s+-rf",  # Sudo dangerous rm
    r"chmod\s+777\s+/",  # Dangerous chmod on root
    r"chown\s+.*\s+/",  # Dangerous chown on root
]


def _is_safe_command(command: str) -> bool:
    """Check if a command is safe to execute.

    Args:
        command: The bash command to check

    Returns:
        bool: True if command appears safe, False otherwise
    """
    if not command.strip():
        return False

    # Check against dangerous patterns
    for pattern in DANGEROUS_PATTERNS:
        if re.search(pattern, command, re.IGNORECASE):
            return False

    return True


@tool(
    description="Execute a bash command and return its output",
    parameters={
        "type": "object",
        "properties": {
            "command": {"type": "string", "description": "The bash command to execute"},
            "timeout": {
                "type": "integer",
                "description": "Timeout in seconds (default: 30, max: 300)",
                "default": 30,
            },
        },
        "required": ["command"],
    },
)
def execute_bash(command: str, timeout: int = 30) -> str:
    """Execute a bash command and return its output.

    Args:
        command: The bash command to execute
        timeout: Timeout in seconds (default: 30, max: 300)

    Returns:
        str: The command output or error message
    """
    # Validate timeout
    if timeout > 300:
        return "Error: Timeout cannot exceed 300 seconds (5 minutes)"

    if timeout < 1:
        return "Error: Timeout must be at least 1 second"

    # Safety check
    if not _is_safe_command(command):
        return f"Error: Command '{command}' contains potentially dangerous operations and has been blocked for safety"

    try:
        # Execute the command
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=str(Path.cwd()),
        )

        # Format output
        output_parts = []

        if result.stdout:
            output_parts.append(f"STDOUT:\n{result.stdout.strip()}")

        if result.stderr:
            output_parts.append(f"STDERR:\n{result.stderr.strip()}")

        if result.returncode != 0:
            output_parts.append(f"Exit code: {result.returncode}")

        if not output_parts:
            output_parts.append("(No output)")

        return f"Command: {command}\n\n" + "\n\n".join(output_parts)

    except subprocess.TimeoutExpired:
        return f"Error: Command '{command}' timed out after {timeout} seconds"

    except Exception as e:
        return f"Error executing command '{command}': {str(e)}"


@tool(
    description="Execute a bash command in a specific directory",
    parameters={
        "type": "object",
        "properties": {
            "command": {"type": "string", "description": "The bash command to execute"},
            "working_directory": {
                "type": "string",
                "description": "The directory to execute the command in",
            },
            "timeout": {
                "type": "integer",
                "description": "Timeout in seconds (default: 30, max: 300)",
                "default": 30,
            },
        },
        "required": ["command", "working_directory"],
    },
)
def execute_bash_in_dir(command: str, working_directory: str, timeout: int = 30) -> str:
    """Execute a bash command in a specific directory.

    Args:
        command: The bash command to execute
        working_directory: The directory to execute the command in
        timeout: Timeout in seconds (default: 30, max: 300)

    Returns:
        str: The command output or error message
    """
    # Validate timeout
    if timeout > 300:
        return "Error: Timeout cannot exceed 300 seconds (5 minutes)"

    if timeout < 1:
        return "Error: Timeout must be at least 1 second"

    # Safety check
    if not _is_safe_command(command):
        return f"Error: Command '{command}' contains potentially dangerous operations and has been blocked for safety"

    # Validate working directory
    work_dir = Path(working_directory).expanduser().resolve()
    if not work_dir.exists():
        return f"Error: Directory '{working_directory}' does not exist"

    if not work_dir.is_dir():
        return f"Error: '{working_directory}' is not a directory"

    try:
        # Execute the command in the specified directory
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=str(work_dir),
        )

        # Format output
        output_parts = []
        output_parts.append(f"Working directory: {work_dir}")

        if result.stdout:
            output_parts.append(f"STDOUT:\n{result.stdout.strip()}")

        if result.stderr:
            output_parts.append(f"STDERR:\n{result.stderr.strip()}")

        if result.returncode != 0:
            output_parts.append(f"Exit code: {result.returncode}")

        if len(output_parts) == 1:  # Only working directory was added
            output_parts.append("(No output)")

        return f"Command: {command}\n\n" + "\n\n".join(output_parts)

    except subprocess.TimeoutExpired:
        return f"Error: Command '{command}' timed out after {timeout} seconds"

    except Exception as e:
        return f"Error executing command '{command}' in '{working_directory}': {str(e)}"


@tool(
    description="Get the current working directory",
    parameters={"type": "object", "properties": {}, "required": []},
)
def get_current_directory() -> str:
    """Get the current working directory.

    Returns:
        str: The current working directory path
    """
    return f"Current working directory: {Path.cwd()}"


@tool(
    description="List files and directories in the current or specified directory",
    parameters={
        "type": "object",
        "properties": {
            "directory": {
                "type": "string",
                "description": "Directory to list (default: current directory)",
            },
            "show_hidden": {
                "type": "boolean",
                "description": "Whether to show hidden files (default: false)",
            },
        },
        "required": [],
    },
)
def list_directory(directory: str = ".", show_hidden: bool = False) -> str:
    """List files and directories.

    Args:
        directory: Directory to list (default: current directory)
        show_hidden: Whether to show hidden files (default: false)

    Returns:
        str: List of files and directories
    """
    try:
        path = Path(directory).expanduser().resolve()

        if not path.exists():
            return f"Error: Directory '{directory}' does not exist"

        if not path.is_dir():
            return f"Error: '{directory}' is not a directory"

        items = []

        try:
            for item in sorted(path.iterdir()):
                if not show_hidden and item.name.startswith("."):
                    continue

                if item.is_dir():
                    items.append(f"[DIR]  {item.name}/")
                else:
                    size = item.stat().st_size
                    if size < 1024:
                        size_str = f"{size}B"
                    elif size < 1024 * 1024:
                        size_str = f"{size/1024:.1f}KB"
                    else:
                        size_str = f"{size/(1024*1024):.1f}MB"
                    items.append(f"[FILE] {item.name} ({size_str})")

        except PermissionError:
            return f"Error: Permission denied accessing '{directory}'"

        if not items:
            return f"Directory '{path}' is empty"

        return f"Contents of '{path}':\n\n" + "\n".join(items)

    except Exception as e:
        return f"Error listing directory '{directory}': {str(e)}"
