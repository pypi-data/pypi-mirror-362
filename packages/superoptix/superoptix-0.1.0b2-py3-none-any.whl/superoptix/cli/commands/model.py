"""
SuperOptiX Model Intelligence System - CLI commands for model management.
"""

from typing import Optional

import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.columns import Columns
from rich.text import Text
import sys


console = Console()
from ...models.manager import SuperOptiXModelManager
from ...models.utils import (
    SuperOptiXBackendType, 
    SuperOptiXModelSize, 
    SuperOptiXModelTask,
    SuperOptiXModelStatus,
    SuperOptiXModelFilter,
    get_superoptix_model_discovery_guide
)
from ...models.config import (
    get_superoptix_model_discovery_settings
)

app = typer.Typer(name="model", help="🚀 SuperOptiX Model Intelligence System")


@app.command("list")
def list_models(
    backend: Optional[str] = typer.Option(None, "--backend", "-b", help="Filter by backend (ollama, mlx, huggingface, lmstudio)"),
    size: Optional[str] = typer.Option(None, "--size", "-s", help="Filter by size (tiny, small, medium, large)"),
    task: Optional[str] = typer.Option(None, "--task", "-t", help="Filter by task (chat, code, reasoning, embedding)"),
    installed_only: bool = typer.Option(True, "--installed-only", help="Show only installed models"),
    all_models: bool = typer.Option(False, "--all", help="Show all available models (overrides --installed-only)"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show detailed information"),
):
    """📋 List SuperOptiX models (installed by default)."""
    
    # Create filter
    filter_obj = SuperOptiXModelFilter(
        backend=SuperOptiXBackendType(backend) if backend else None,
        size=SuperOptiXModelSize(size) if size else None,
        task=SuperOptiXModelTask(task) if task else None,
        installed_only=not all_models if not all_models else False,
    )
    
    # Get models
    manager = SuperOptiXModelManager()
    models = manager.list_models(filter_obj)
    
    if not models:
        if all_models:
            console.print("❌ No models found matching your criteria.")
        else:
            console.print("🤖 No installed models found.")
            console.print("🔍 Discover models: [bold]super model discover[/bold]")
            console.print("📥 Install a model: [bold]super model install <model_name>[/bold]")
        return
    
    # Create table
    table = Table(
        title=f"🚀 SuperOptiX Model Intelligence - {len(models)} models",
        show_header=True,
        header_style="bold cyan",
        border_style="blue",
    )
    
    table.add_column("Model", style="bold white", no_wrap=True)
    table.add_column("Backend", style="cyan", justify="center")
    table.add_column("Status", style="green", justify="center")
    table.add_column("Size", style="yellow", justify="center")
    table.add_column("Task", style="magenta", justify="center")
    
    if verbose:
        table.add_column("Parameters", style="dim", justify="center")
        table.add_column("Disk Size", style="dim", justify="center")
        table.add_column("Last Used", style="dim", justify="center")
    
    # Add rows
    for model in models:
        status_emoji = {
            SuperOptiXModelStatus.INSTALLED: "✅",
            SuperOptiXModelStatus.DOWNLOADING: "⬇️",
            SuperOptiXModelStatus.FAILED: "❌",
            SuperOptiXModelStatus.UNKNOWN: "❓",
        }.get(model.status, "❓")
        
        row = [
            model.name,
            f"🦙 {model.backend.value}" if model.backend == SuperOptiXBackendType.OLLAMA else
            f"🍎 {model.backend.value}" if model.backend == SuperOptiXBackendType.MLX else
            f"🤗 {model.backend.value}" if model.backend == SuperOptiXBackendType.HUGGINGFACE else
            f"🎮 {model.backend.value}" if model.backend == SuperOptiXBackendType.LMSTUDIO else
            model.backend.value,
            f"{status_emoji} {model.status.value}",
            model.size.value if model.size else "Unknown",
            model.task.value if model.task else "General",
        ]
        
        if verbose:
            row.extend([
                model.parameters or "Unknown",
                f"{model.size_gb:.1f}GB" if model.size_gb else "Unknown",
                model.last_used.strftime("%Y-%m-%d") if model.last_used else "Never",
            ])
        
        table.add_row(*row)
    
    console.print(table)
    # Always show discovery and install guidance
    console.print()
    console.print("🔍 Discover more models: [bold]super model discover[/bold]")
    console.print("📥 Install a model: [bold]super model install <model_name>[/bold]")


@app.command("discover")
def discover_models():
    """🔍 SuperOptiX Model Discovery Guide."""
    _show_discovery_guide()


@app.command("guide")
def model_guide():
    """📚 SuperOptiX Model Installation Guide."""
    _show_detailed_guide()


@app.command("install")
def install_model(
    model_name: str = typer.Argument(..., help="Model name to install"),
    backend: Optional[str] = typer.Option(None, "--backend", "-b", help="Specific backend to use"),
    force: bool = typer.Option(False, "--force", "-f", help="Force reinstall if already exists"),
):
    """📥 Install a SuperOptiX model."""
    
    console.print(f"🚀 SuperOptiX Model Intelligence - Installing [bold cyan]{model_name}[/bold cyan]")
    
    # Parse backend from model name if not specified
    if "/" in model_name and not backend:
        backend_str, model_name = model_name.split("/", 1)
        backend = backend_str
    
    # Use the model manager to handle installation
    manager = SuperOptiXModelManager()
    
    # Determine backend type
    if backend == "ollama" or (not backend and "/" not in model_name):
        backend_type = SuperOptiXBackendType.OLLAMA
    elif backend == "mlx":
        backend_type = SuperOptiXBackendType.MLX
    elif backend == "huggingface":
        backend_type = SuperOptiXBackendType.HUGGINGFACE
    elif backend == "lmstudio":
        backend_type = SuperOptiXBackendType.LMSTUDIO
    else:
        console.print("❌ Please specify a backend or use format: backend/model_name")
        console.print("Supported backends: ollama, mlx, huggingface, lmstudio")
        _show_discovery_guide()
        return
    
    # Install the model using the manager
    success = manager.install_model(model_name, backend_type=backend_type)
    
    if success:
        console.print()
        console.print("🎉 [bold green]Installation completed successfully![/bold green]")
        if backend_type == SuperOptiXBackendType.OLLAMA:
            console.print("🦙 Ollama running on http://localhost:11434 ready to use with SuperOptiX!")
        elif backend_type == SuperOptiXBackendType.MLX:
            console.print("🍎 MLX model ready to use with SuperOptiX!")
        elif backend_type == SuperOptiXBackendType.HUGGINGFACE:
            console.print("🤗 HuggingFace model ready to use with SuperOptiX!")
        elif backend_type == SuperOptiXBackendType.LMSTUDIO:
            console.print("🎮 LM Studio model ready to use with SuperOptiX!")
    else:
        console.print()
        console.print("❌ [bold red]Installation failed![/bold red]")
        console.print("Check the error messages above for details.")
        console.print()
        console.print("💡 [bold]Troubleshooting:[/bold]")
        console.print("  • Run [bold]super model backends[/bold] to check backend status")
        console.print("  • Run [bold]super model guide[/bold] for installation instructions")


@app.command("info")
def model_info(
    model_name: str = typer.Argument(..., help="Model name to get info about"),
):
    """ℹ️ Get detailed information about a SuperOptiX model."""
    
    manager = SuperOptiXModelManager()
    models = manager.list_models()
    
    # Find the model
    model = None
    for m in models:
        if m.name == model_name or m.full_name == model_name:
            model = m
            break
    
    if not model:
        console.print(f"❌ Model [bold]{model_name}[/bold] not found.")
        console.print("Use [bold]super model list[/bold] to see available models.")
        return
    
    # Create info panel
    info_text = f"""
[bold]Name:[/bold] {model.name}
[bold]Backend:[/bold] {model.backend.value}
[bold]Status:[/bold] {model.status.value}
[bold]Size:[/bold] {model.size.value if model.size else 'Unknown'}
[bold]Task:[/bold] {model.task.value if model.task else 'General'}
[bold]Parameters:[/bold] {model.parameters or 'Unknown'}
[bold]Disk Size:[/bold] {f"{model.size_gb:.1f}GB" if model.size_gb else 'Unknown'}
[bold]Usage Count:[/bold] {model.usage_count}
[bold]Last Used:[/bold] {model.last_used.strftime("%Y-%m-%d %H:%M") if model.last_used else 'Never'}
"""
    
    if model.description:
        info_text += f"\n[bold]Description:[/bold] {model.description}"
    
    if model.tags:
        info_text += f"\n[bold]Tags:[/bold] {', '.join(model.tags)}"
    
    panel = Panel(
        info_text.strip(),
        title=f"🚀 SuperOptiX Model Info - {model.display_name}",
        border_style="blue",
    )
    
    console.print(panel)


@app.command("backends")
def list_backends():
    """🔧 Show SuperOptiX backend status."""
    
    manager = SuperOptiXModelManager()
    backends = manager.get_backend_info()
    
    table = Table(
        title="🔧 SuperOptiX Backend Status",
        show_header=True,
        header_style="bold cyan",
        border_style="blue",
    )
    
    table.add_column("Backend", style="bold white")
    table.add_column("Status", style="green", justify="center")
    table.add_column("Version", style="yellow", justify="center")
    table.add_column("Models", style="magenta", justify="center")
    table.add_column("Configuration", style="dim")
    
    for backend in backends:
        status_emoji = "✅" if backend.available else "❌"
        status_text = f"{status_emoji} {backend.status}"
        
        config_text = ""
        if backend.host and backend.port:
            config_text = f"{backend.host}:{backend.port}"
        elif backend.host:
            config_text = backend.host
        
        table.add_row(
            f"{'🦙' if backend.type == SuperOptiXBackendType.OLLAMA else '🍎' if backend.type == SuperOptiXBackendType.MLX else '🤗' if backend.type == SuperOptiXBackendType.HUGGINGFACE else '🎮' if backend.type == SuperOptiXBackendType.LMSTUDIO else ''} {backend.type.value}",
            status_text,
            backend.version or "Unknown",
            str(backend.models_count),
            config_text,
        )
    
    console.print(table)


@app.command("dspy")
def create_dspy_client(
    model_name: str = typer.Argument(..., help="Model name for DSPy client"),
    temperature: float = typer.Option(0.7, "--temperature", "-t", help="Temperature for generation"),
    max_tokens: int = typer.Option(2048, "--max-tokens", "-m", help="Maximum tokens"),
):
    """🧠 Create a DSPy client for SuperOptiX model."""
    
    manager = SuperOptiXModelManager()
    
    try:
        client = manager.create_dspy_client(model_name, temperature=temperature, max_tokens=max_tokens)
        console.print(f"✅ Created DSPy client for [bold cyan]{model_name}[/bold cyan]")
        console.print(f"Client type: [bold]{type(client).__name__}[/bold]")
        console.print()
        console.print("Example usage:")
        console.print("  [dim]import dspy[/dim]")
        console.print("  [dim]dspy.configure(lm=client)[/dim]")
        
    except Exception as e:
        console.print(f"❌ Failed to create DSPy client: {e}")


@app.command("server")
def start_server(
    backend: str = typer.Argument(..., help="Backend type (mlx, huggingface, lmstudio)"),
    model_name: str = typer.Argument(..., help="Model name to start server for"),
    port: int = typer.Option(None, "--port", "-p", help="Port to run server on"),
):
    """🚀 Start a local server for SuperOptiX models.
    
    Examples:
      super model server mlx mlx-community/Llama-3.2-3B-Instruct-4bit
      super model server huggingface microsoft/DialoGPT-small --port 8001
      super model server lmstudio llama-3.2-1b-instruct
      
    Backends:
      mlx          Apple Silicon optimized (default: port 8000)
      huggingface  Transformers models (default: port 8001)  
      lmstudio     Desktop app models (default: port 1234)
      
    Note: Ollama servers use 'ollama serve' command separately.
    """
    
    # Custom help handler
    if any(flag in sys.argv for flag in ["--help", "-h"]):
        try:
            console = Console()
            help_text = Text()
            help_text.append("\n🚀 Start local model servers for MLX, HuggingFace, or LM Studio.\n\n", style="bold cyan")
            help_text.append("Examples:\n", style="bold yellow")
            help_text.append("  super model server mlx mlx-community/Llama-3.2-3B-Instruct-4bit\n", style="white")
            help_text.append("  super model server huggingface microsoft/DialoGPT-small --port 8001\n", style="white")
            help_text.append("  super model server lmstudio llama-3.2-1b-instruct\n\n", style="white")
            help_text.append("Backends:\n", style="bold yellow")
            help_text.append("  mlx         Apple Silicon (default: 8000)\n", style="white")
            help_text.append("  huggingface Transformers (default: 8001)\n", style="white")
            help_text.append("  lmstudio    Desktop app (default: 1234)\n\n", style="white")
            help_text.append("Note: Ollama uses 'ollama serve' separately.\n", style="bold magenta")
            panel = Panel(help_text, title="super model server", border_style="blue")
            console.print(panel)
        except Exception:
            print("\n🚀 Start local model servers for MLX, HuggingFace, or LM Studio.\n")
            print("Examples:")
            print("  super model server mlx mlx-community/Llama-3.2-3B-Instruct-4bit")
            print("  super model server huggingface microsoft/DialoGPT-small --port 8001")
            print("  super model server lmstudio llama-3.2-1b-instruct\n")
            print("Backends:")
            print("  mlx         Apple Silicon (default: 8000)")
            print("  huggingface Transformers (default: 8001)")
            print("  lmstudio    Desktop app (default: 1234)\n")
            print("Note: Ollama uses 'ollama serve' separately.\n")
        sys.exit(0)

    if backend.lower() == "mlx":
        if port is None:
            port = 8000
        start_mlx_server(model_name, port)
    elif backend.lower() == "huggingface":
        if port is None:
            port = 8001
        start_huggingface_server(model_name, port)
    elif backend.lower() == "lmstudio":
        if port is None:
            port = 1234
        start_lmstudio_server(model_name, port)
    else:
        console.print(f"❌ Unsupported backend: [bold red]{backend}[/bold red]")
        console.print("Supported backends: mlx, huggingface, lmstudio")


def start_mlx_server(model_name: str, port: int = 8000):
    """Start a local MLX server for the specified model."""
    console.print()
    console.print("🍎 [bold]MLX Local Server[/bold]")
    console.print(f"Starting MLX server for [bold cyan]{model_name}[/bold cyan] on port {port}...")
    
    # Check if model is installed
    manager = SuperOptiXModelManager()
    installed_models = manager.list_models(SuperOptiXModelFilter(backend=SuperOptiXBackendType.MLX))
    
    model_found = False
    for model in installed_models:
        if model.name == model_name or model.name.replace("_", "/") == model_name:
            model_found = True
            break
    
    if not model_found:
        console.print(f"❌ Model [bold red]{model_name}[/bold red] not found in installed MLX models")
        console.print("💡 Install the model first: [bold]super model install -b mlx <model_name>[/bold]")
        return False
    
    console.print("🚀 Starting MLX server...")
    console.print(f"📡 Server will be available at: [bold green]http://localhost:{port}[/bold green]")
    console.print("💡 Use this URL in your playbook's api_base configuration")
    console.print()
    console.print("🔧 Manual server startup command:")
    console.print(f"   python -m mlx_lm.server --model {model_name} --port {port}")
    console.print()
    console.print("📋 Example playbook configuration:")
    console.print(f"""   language_model:
     provider: mlx
     model: {model_name}
     api_base: http://localhost:{port}""")
    
    # Actually start the MLX server
    try:
        import subprocess
        import sys
        
        # Start the MLX server as a subprocess
        cmd = [sys.executable, "-m", "mlx_lm.server", "--model", model_name, "--port", str(port)]
        
        console.print(f"🔄 Executing: {' '.join(cmd)}")
        console.print("⏳ Server is starting... (Press Ctrl+C to stop)")
        
        # Run the server process
        subprocess.run(cmd, check=True)
        
    except subprocess.CalledProcessError as e:
        console.print(f"❌ Failed to start MLX server: {e}")
        console.print("💡 Make sure mlx-lm is installed: pip install mlx-lm")
        return False
    except KeyboardInterrupt:
        console.print("\n🛑 MLX server stopped by user")
        return True
    except Exception as e:
        console.print(f"❌ Unexpected error starting MLX server: {e}")
        return False
    
    return True

def start_huggingface_server(model_name: str, port: int = 8001):
    """Start a local HuggingFace server for the specified model."""
    console.print()
    console.print("🤗 [bold]HuggingFace Local Server[/bold]")
    console.print(f"Starting HuggingFace server for [bold cyan]{model_name}[/bold cyan] on port {port}...")
    
    try:
        # Import and start the HuggingFace server
        from superoptix.models.backends.huggingface_server import start_huggingface_server as start_hf_server
        
        console.print("🚀 Starting HuggingFace server...")
        console.print(f"📡 Server will be available at: [bold green]http://localhost:{port}[/bold green]")
        console.print("💡 Use this URL in your playbook's api_base configuration")
        console.print()
        console.print("🔧 Manual server startup command:")
        console.print(f"   python -m superoptix.models.backends.huggingface_server {model_name} --port {port}")
        console.print()
        console.print("📋 Example playbook configuration:")
        console.print(f"""   language_model:
     provider: huggingface
     model: {model_name}
     api_base: http://localhost:{port}""")
        
        # Start the server
        start_hf_server(model_name, port)
        
    except ImportError as e:
        console.print(f"❌ Failed to import HuggingFace server: {e}")
        console.print("💡 Make sure you have the required dependencies:")
        console.print("   pip install fastapi uvicorn torch transformers")
        console.print("   or")
        console.print("   uv pip install fastapi uvicorn torch transformers")
        return False
    except Exception as e:
        console.print(f"❌ Failed to start HuggingFace server: {e}")
        return False
    
    return True


def start_lmstudio_server(model_name: str, port: int = 1234):
    """Start a local LM Studio server for the specified model."""
    console.print()
    console.print("🎮 [bold]LM Studio Local Server[/bold]")
    console.print(f"Starting LM Studio server for [bold cyan]{model_name}[/bold cyan] on port {port}...")
    
    # Import the LM Studio backend
    from superoptix.models.backends.lmstudio import SuperOptiXLMStudioBackend
    
    # Create backend instance
    backend = SuperOptiXLMStudioBackend()
    
    # Check if LM Studio CLI is available
    if not backend.is_available_sync():
        console.print("❌ LM Studio CLI is not available on your system.")
        console.print()
        console.print("📥 [bold]Install LM Studio:[/bold]")
        console.print("  🌐 Visit: [bold cyan]https://lmstudio.ai[/bold cyan]")
        console.print("  📥 Download and install for your platform")
        console.print("  🔧 The lms CLI will be available after installation")
        console.print()
        console.print("💡 After installing LM Studio, run this command again:")
        console.print(f"  [bold green]super model server lmstudio {model_name}[/bold green]")
        return False
    
    # Get installed models
    try:
        installed_models = backend.list_installed_models_sync()
    except Exception as e:
        console.print(f"❌ Failed to list installed models: {e}")
        return False
    
    # Check for exact match first
    exact_match = None
    for model in installed_models:
        if model.name == model_name:
            exact_match = model
            break
    
    if exact_match:
        # Exact match found - load and start server
        console.print(f"✅ Found exact match: [bold green]{exact_match.name}[/bold green]")
        console.print()
        console.print("🔄 Loading model and starting server...")
        
        try:
            # Load the model
            backend._run_lms_command(["load", exact_match.name])
            console.print(f"✅ Model [bold green]{exact_match.name}[/bold green] loaded successfully!")
            
            # Start the server
            console.print("🚀 Starting LM Studio server...")
            console.print(f"📡 Server will be available at: [bold green]http://localhost:{port}[/bold green]")
            console.print()
            console.print("💡 The server is now running in the background.")
            console.print("🎯 You can now use this model with SuperOptiX:")
            console.print(f"  [bold green]super model dspy lmstudio/{exact_match.name}[/bold green]")
            console.print()
            console.print("📋 Example playbook configuration:")
            console.print(f"""   language_model:
     provider: lmstudio
     model: {exact_match.name}
     api_base: http://localhost:{port}""")
            console.print()
            console.print("🛑 To stop the server, use Ctrl+C or close the LM Studio application")
            
            # Start the server process
            import subprocess
            
            # Start lms server start command
            cmd = ["lms", "server", "start"]
            console.print(f"🔄 Executing: {' '.join(cmd)}")
            console.print("⏳ Server is starting... (Press Ctrl+C to stop)")
            
            # Run the server process
            subprocess.run(cmd, check=True)
            
        except subprocess.CalledProcessError as e:
            console.print(f"❌ Failed to start LM Studio server: {e}")
            console.print("💡 Make sure LM Studio is properly installed and configured")
            return False
        except KeyboardInterrupt:
            console.print("\n🛑 LM Studio server stopped by user")
            return True
        except Exception as e:
            console.print(f"❌ Unexpected error: {e}")
            return False
        
        return True
    
    else:
        # No exact match - show fuzzy matching
        console.print(f"❌ No exact match found for [bold red]{model_name}[/bold red]")
        console.print()
        console.print("🔍 [bold]Available LM Studio models:[/bold]")
        
        if not installed_models:
            console.print("❌ No models found in LM Studio.")
            console.print("💡 Install models first using the LM Studio application")
            console.print("   or use: [bold green]super model install -b lmstudio <model_name>[/bold green]")
            return False
        
        # Show available models in a table
        from rich.table import Table
        
        table = Table(
            title="🎮 Available LM Studio Models",
            show_header=True,
            header_style="bold cyan",
            border_style="blue",
        )
        
        table.add_column("Model Name", style="bold white", no_wrap=True)
        table.add_column("Size", style="yellow", justify="center")
        table.add_column("Task", style="magenta", justify="center")
        table.add_column("Parameters", style="dim", justify="center")
        
        for i, model in enumerate(installed_models, 1):
            table.add_row(
                f"{i}. {model.name}",
                model.size.value if model.size else "Unknown",
                model.task.value if model.task else "General",
                model.parameters or "Unknown"
            )
        
        console.print(table)
        console.print()
        console.print("💡 [bold]To use a specific model:[/bold]")
        console.print("  • Use the exact model name from the list above")
        console.print("  • Example: [bold green]super model server lmstudio llama-3.2-1b-instruct[/bold green]")
        console.print()
        console.print("🔍 [bold]Fuzzy matching examples:[/bold]")
        console.print("  • 'llama3.2' → Look for models containing 'llama3.2'")
        console.print("  • 'llama' → Look for models containing 'llama'")
        console.print("  • '3b' → Look for models containing '3b'")
        
        # Show fuzzy matches if any
        fuzzy_matches = []
        model_name_lower = model_name.lower()
        for model in installed_models:
            if model_name_lower in model.name.lower():
                fuzzy_matches.append(model)
        
        if fuzzy_matches:
            console.print()
            console.print("🎯 [bold]Fuzzy matches found:[/bold]")
            for i, model in enumerate(fuzzy_matches, 1):
                console.print(f"  {i}. [bold green]{model.name}[/bold green]")
            console.print()
            console.print("💡 Use one of the exact model names above:")
            for model in fuzzy_matches:
                console.print(f"  [bold green]super model server lmstudio {model.name}[/bold green]")
        else:
            console.print()
            console.print("❌ [bold]No fuzzy matches found for '{model_name}'[/bold]")
            console.print("💡 Try a different search term or install the model first:")
            console.print("   [bold green]super model install -b lmstudio <model_name>[/bold green]")
        
        return False


def _show_discovery_guide():
    """Show the SuperOptiX model discovery guide."""
    guide = get_superoptix_model_discovery_guide()
    
    console.print()
    console.print("🔍 [bold cyan]SuperOptiX Model Discovery Guide[/bold cyan]")
    console.print()
    
    panels = []
    for backend_name, info in guide.items():
        content = f"""
[bold]Description:[/bold] {info['description']}

[bold]Example Models:[/bold]
{info['popular_models']}

[bold]Benefits:[/bold]
{info['benefits']}

[bold]Browse:[/bold] {info['browse_url']}
[bold]Install:[/bold] {info['install_cmd']}
"""
        
        panel = Panel(
            content.strip(),
            title=info['name'],
            border_style="blue",
        )
        panels.append(panel)
    
    console.print(Columns(panels))
    
    console.print()
    console.print("🚀 [bold cyan]Example Commands for Each Backend[/bold cyan]")
    console.print()
    
    # Ollama Examples
    console.print("🦙 [bold]Ollama (Local Models):[/bold]")
    console.print("  [yellow]Install Ollama:[/yellow]")
    console.print("    curl -fsSL https://ollama.com/install.sh | sh")
    console.print("  [yellow]Install a model:[/yellow]")
    console.print("    ollama pull llama3.2:3b")
    console.print("  [yellow]Use with SuperOptiX:[/yellow]")
    console.print("    super model dspy ollama/llama3.2:3b")
    console.print()
    
    # MLX Examples
    console.print("🍎 [bold]MLX (Apple Silicon):[/bold]")
    console.print("  [yellow]Install a model:[/yellow]")
    console.print("    super model install -b mlx mlx-community/Llama-3.2-3B-Instruct-4bit")
    console.print("  [yellow]Start a local server:[/yellow]")
    console.print("    super model server mlx mlx-community/Llama-3.2-3B-Instruct-4bit --port 8000")
    console.print("  [yellow]Use with SuperOptiX:[/yellow]")
    console.print("    super model dspy mlx-community/Llama-3.2-3B-Instruct-4bit")
    console.print()
    
    # HuggingFace Examples
    console.print("🤗 [bold]HuggingFace (Transformers):[/bold]")
    console.print("  [yellow]Install a model:[/yellow]")
    console.print("    super model install -b huggingface microsoft/Phi-4")
    console.print("  [yellow]Start a local server:[/yellow]")
    console.print("    super model server huggingface microsoft/Phi-4 --port 8001")
    console.print("  [yellow]Use with SuperOptiX:[/yellow]")
    console.print("    super model dspy microsoft/Phi-4")
    console.print()
    
    # LM Studio Examples
    console.print("🎮 [bold]LM Studio (Desktop App):[/bold]")
    console.print("  [yellow]Install a model:[/yellow]")
    console.print("    Download via the LM Studio app")
    console.print("  [yellow]Start a local server:[/yellow]")
    console.print("    Start server in LM Studio app (usually runs on localhost:1234)")
    console.print("  [yellow]Use with SuperOptiX:[/yellow]")
    console.print("    super model dspy lmstudio/your-model-name")
    console.print()
    
    console.print("💡 [bold]Quick Start:[/bold]")
    console.print("  1. Choose a backend above")
    console.print("  2. Browse their model library")
    console.print("  3. Install models using their tools")
    console.print("  4. Use [bold]super model list[/bold] to see installed models")


def _show_detailed_guide():
    """Show detailed installation guide."""
    settings = get_superoptix_model_discovery_settings()
    
    console.print("📚 [bold cyan]SuperOptiX Model Installation Guide[/bold cyan]")
    console.print()
    
    for backend_name, guide_info in settings["guides"].items():
        console.print(f"## {guide_info['title']}")
        console.print(f"{guide_info['description']}")
        console.print()
        
        console.print("### Quick Start:")
        for step in guide_info['quick_start']:
            console.print(f"  {step}")
        console.print()
        
        console.print("### Popular Models:")
        for model in guide_info['popular_models']:
            console.print(f"  • {model}")
        console.print()
        console.print("---")
        console.print()
    
    console.print("🔍 [bold]Want to explore?[/bold]")
    console.print("  Use [bold]super model discover[/bold] for the interactive guide")


if __name__ == "__main__":
    app() 