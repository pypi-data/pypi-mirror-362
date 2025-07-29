"""Basic built-in tools for LoopLM."""

from datetime import datetime
from pathlib import Path

from looplm.tools.base import tool


@tool(description="Get the current date and time")
def get_current_time() -> str:
    """Get the current date and time in a human-readable format."""
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S %Z")


@tool(description="Read the contents of a text file")
def read_file(file_path: str, max_lines: int = 100) -> str:
    """Read the contents of a text file.

    Args:
        file_path: Path to the file to read
        max_lines: Maximum number of lines to read (default: 100)
    """
    try:
        target_path = Path(file_path).expanduser().resolve()

        if not target_path.exists():
            return f"Error: File '{file_path}' does not exist"

        if not target_path.is_file():
            return f"Error: '{file_path}' is not a file"

        # Check file size (limit to 1MB)
        if target_path.stat().st_size > 1024 * 1024:
            return f"Error: File '{file_path}' is too large (>1MB)"

        with target_path.open("r", encoding="utf-8", errors="ignore") as f:
            lines = []
            for i, line in enumerate(f):
                if i >= max_lines:
                    lines.append(f"\n... (truncated after {max_lines} lines)")
                    break
                lines.append(line.rstrip())

        return f"Contents of '{file_path}':\n" + "\n".join(lines)

    except PermissionError:
        return f"Error: Permission denied reading '{file_path}'"
    except UnicodeDecodeError:
        return f"Error: '{file_path}' is not a text file or uses unsupported encoding"
    except Exception as e:
        return f"Error reading file '{file_path}': {str(e)}"
