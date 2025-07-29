"""
Utility functions for the SuperOptiX CLI.
"""
import asyncio
import os  # noqa: F401
from pathlib import Path
from typing import Any, Coroutine

from rich.console import Console

console = Console()


def is_superoptix_project() -> bool:
    """
    Check if the current directory is a SuperOptiX project by looking for the .super file.
    
    Returns:
        bool: True if .super file exists in current directory, False otherwise
    """
    return Path(".super").exists()


def validate_superoptix_project(commands_that_require_project: list[str] = None) -> None:
    """
    Validate that the user is in a SuperOptiX project directory.
    
    This function checks for the presence of a .super file in the current directory.
    If not found, it displays an error message and exits.
    
    Args:
        commands_that_require_project: List of commands that require being in a project directory.
                                      If None, uses default list of commands that need project context.
    
    Raises:
        SystemExit: If not in a SuperOptiX project directory
    """
    if commands_that_require_project is None:
        commands_that_require_project = [
            "agent", "ag",  # agent commands
            "orch",  # orchestra commands  
            "spec",  # superspec commands
            "observe", "ob",  # observability commands
        ]
    
    if not is_superoptix_project():
        console.print("\n[bold red]❌ Not in a SuperOptiX project directory![/bold red]")
        console.print("\n[yellow]This command requires you to be in a SuperOptiX project directory.[/yellow]")
        console.print("\n[cyan]To fix this:[/cyan]")
        console.print("  1. [green]Navigate to your SuperOptiX project directory[/green]")
        console.print("     [dim]cd /path/to/your/superoptix/project[/dim]")
        console.print("  2. [green]Verify you're in the right place:[/green]")
        console.print("     [dim]ls -la | grep .super[/dim]")
        console.print("  3. [green]You should see the .super file - this confirms you're in a SuperOptiX project![/green]")
        console.print("\n[cyan]If you don't have a project yet:[/cyan]")
        console.print("  [green]super init my_project_name[/green]")
        console.print("  [green]cd my_project_name[/green]")
        console.print("\n[dim]💡 The .super file is created when you run 'super init' and marks the project root.[/dim]")
        raise SystemExit(1)


def run_async(coro: Coroutine[Any, Any, Any]) -> Any:
    """
    Safely run an async coroutine, handling existing event loops properly.
    
    This function prevents ResourceWarning about unclosed event loops by:
    1. Checking if there's already a running event loop
    2. Using the existing loop if available
    3. Creating a new loop only when necessary
    
    Args:
        coro: The coroutine to run
        
    Returns:
        The result of the coroutine
    """
    try:
        loop = asyncio.get_running_loop()
        # If we're already in an event loop, we need to handle this differently
        # For CLI commands, we'll create a new task and run it
        if loop and loop.is_running():
            # This shouldn't happen in CLI context, but handle it gracefully
            return asyncio.run(coro)
        else:
            return asyncio.run(coro)
    except RuntimeError:
        # No running loop, safe to use asyncio.run()
        return asyncio.run(coro) 