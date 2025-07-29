"""
SuperOptiX Model Intelligence System - MLX backend implementation.
"""

import platform
import re
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict, Any
from rich.console import Console

from ..utils import (
    SuperOptiXModelInfo, 
    SuperOptiXBackendInfo, 
    SuperOptiXModelStatus, 
    SuperOptiXBackendType, 
    SuperOptiXModelSize, 
    SuperOptiXModelTask
)
from .base import SuperOptiXBaseBackend

console = Console()


class SuperOptiXMLXBackend(SuperOptiXBaseBackend):
    """SuperOptiX MLX backend for Apple Silicon model management."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cache_dir = Path(kwargs.get("cache_dir", "~/.cache/mlx-models")).expanduser()
        self.default_quantization = kwargs.get("default_quantization", "4bit")
        
    @property
    def backend_type(self) -> SuperOptiXBackendType:
        return SuperOptiXBackendType.MLX

    def is_available(self) -> bool:
        """Check if MLX is available (Apple Silicon only)."""
        try:
            # Check if we're on Apple Silicon
            if platform.system() != "Darwin" or platform.machine() != "arm64":
                return False
            
            # Try to import MLX
            import sys
            sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "mlx-lm-latest"))
            import mlx.core as mx  # noqa: F401
            return True
        except ImportError:
            return False

    def get_backend_info(self) -> SuperOptiXBackendInfo:
        """Get SuperOptiX MLX backend information."""
        try:
            if not self.is_available():
                return SuperOptiXBackendInfo(
                    type=self.backend_type,
                    available=False,
                    error="MLX requires Apple Silicon (M1/M2/M3) with macOS",
                    config=self.config,
                )
            
            # Get MLX version
            import sys
            sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "mlx-lm-latest"))
            import mlx
            
            # Count installed models
            installed_models = self.list_installed_models()
            
            return SuperOptiXBackendInfo(
                type=self.backend_type,
                available=True,
                version=getattr(mlx, "__version__", "unknown"),
                status="available",
                models_count=len(installed_models),
                config=self.config,
            )
        except Exception as e:
            return SuperOptiXBackendInfo(
                type=self.backend_type,
                available=False,
                error=str(e),
                config=self.config,
            )

    def list_available_models(self) -> List[SuperOptiXModelInfo]:
        """List all available SuperOptiX MLX models."""
        # Return installed models plus some popular MLX-compatible models
        installed = self.list_installed_models()
        
        # Add popular models that can be converted to MLX
        popular_models = [
            ("mlx-community/Llama-3.2-1B-Instruct-4bit", "1B", SuperOptiXModelSize.TINY, SuperOptiXModelTask.CHAT, "Llama 3.2 1B quantized for MLX"),
            ("mlx-community/Llama-3.2-3B-Instruct-4bit", "3B", SuperOptiXModelSize.SMALL, SuperOptiXModelTask.CHAT, "Llama 3.2 3B quantized for MLX"),
            ("mlx-community/Meta-Llama-3.1-8B-Instruct-4bit", "8B", SuperOptiXModelSize.MEDIUM, SuperOptiXModelTask.CHAT, "Llama 3.1 8B quantized for MLX"),
            ("mlx-community/CodeLlama-7b-Instruct-hf-4bit", "7B", SuperOptiXModelSize.SMALL, SuperOptiXModelTask.CODE, "CodeLlama 7B quantized for MLX"),
            ("mlx-community/Mistral-7B-Instruct-v0.3-4bit", "7B", SuperOptiXModelSize.SMALL, SuperOptiXModelTask.CHAT, "Mistral 7B quantized for MLX"),
            ("mlx-community/Qwen2.5-7B-Instruct-4bit", "7B", SuperOptiXModelSize.SMALL, SuperOptiXModelTask.REASONING, "Qwen 2.5 7B quantized for MLX"),
            ("mlx-community/phi-3-mini-4k-instruct-4bit", "3.8B", SuperOptiXModelSize.SMALL, SuperOptiXModelTask.CHAT, "Phi-3 Mini quantized for MLX"),
        ]
        
        # Track installed model names to avoid duplicates
        installed_names = {model.name for model in installed}
        
        # Add popular models that aren't installed
        for name, params, size, task, desc in popular_models:
            if name not in installed_names:
                installed.append(SuperOptiXModelInfo(
                    name=name,
                    backend=self.backend_type,
                    status=SuperOptiXModelStatus.AVAILABLE,
                    size=size,
                    task=task,
                    description=desc,
                    parameters=params,
                    quantization=self.default_quantization,
                    tags=["popular", "mlx", task.value],
                ))
        
        return installed

    def list_installed_models(self) -> List[SuperOptiXModelInfo]:
        """List installed SuperOptiX MLX models."""
        try:
            if not self.is_available():
                return []
            
            models = []
            
            # Check cache directory for downloaded models
            if self.cache_dir.exists():
                for model_dir in self.cache_dir.iterdir():
                    if model_dir.is_dir() and (model_dir / "config.json").exists():
                        # Parse model info from directory
                        name = model_dir.name
                        
                        # Get directory size
                        disk_size = sum(f.stat().st_size for f in model_dir.rglob('*') if f.is_file())
                        
                        # Infer model characteristics
                        size_category = self._infer_model_size(name)
                        task = self._infer_model_task(name)
                        parameters = self._extract_parameters(name)
                        
                        models.append(SuperOptiXModelInfo(
                            name=name,
                            backend=self.backend_type,
                            status=SuperOptiXModelStatus.INSTALLED,
                            size=size_category,
                            task=task,
                            parameters=parameters,
                            quantization="4bit" if "4bit" in name else None,
                            disk_size=disk_size,
                            local_path=model_dir,
                            tags=["installed", "mlx", task.value if task else "unknown"],
                        ))
            
            return models
        except Exception:
            return []

    def install_model(self, model_name: str, **kwargs) -> bool:
        """Install a SuperOptiX model for MLX."""
        try:
            if not self.is_available():
                from rich.console import Console  # noqa: F401
                from rich.panel import Panel
                from rich.text import Text
                from rich.columns import Columns
                
                # Use the global console instance defined at the top of the module
                
                # Create colorful error message
                error_text = Text("❌ MLX is not available on this system", style="bold red")
                
                # Requirements section
                requirements = Text()
                requirements.append("🔧 MLX requires:\n", style="bold yellow")
                requirements.append("  • Apple Silicon (M1/M2/M3) with macOS\n", style="cyan")
                requirements.append("  • Python 3.9–3.12\n", style="cyan")
                requirements.append("  • The 'mlx' and 'mlx-lm' packages installed\n", style="cyan")
                
                # Installation instructions
                install_text = Text()
                install_text.append("🚀 To install MLX, run:\n", style="bold green")
                install_text.append("  pip install mlx mlx-lm\n", style="bright_white")
                install_text.append("  or (with uv):\n", style="bright_white")
                install_text.append("  uv pip install mlx mlx-lm\n", style="bright_white")
                install_text.append("  or (with conda):\n", style="bright_white")
                install_text.append("  conda install -c apple mlx mlx-lm\n", style="bright_white")
                
                # Next steps
                next_steps = Text()
                next_steps.append("📚 See https://github.com/ml-explore/mlx for more details\n", style="blue")
                next_steps.append("💡 After installation, try: super model install -b mlx <model_name>\n", style="bright_green")
                
                # Create panels
                error_panel = Panel(error_text, border_style="red", title="🍎 MLX Setup Required")
                req_panel = Panel(requirements, border_style="yellow", title="📋 Requirements")
                install_panel = Panel(install_text, border_style="green", title="⚡ Installation")
                next_panel = Panel(next_steps, border_style="blue", title="🎯 Next Steps")
                
                # Display in columns for better layout
                console.print()
                console.print(error_panel)
                console.print()
                console.print(Columns([req_panel, install_panel]))
                console.print()
                console.print(next_panel)
                console.print()
                
                return False
            
            console.print(f"Starting download of {model_name} for MLX...")
            
            # Use HuggingFace Hub to download the model
            try:
                from huggingface_hub import snapshot_download
                
                # Download the model
                model_path = self.cache_dir / model_name.replace("/", "_")
                model_path.mkdir(parents=True, exist_ok=True)
                
                console.print(f"Downloading to {model_path}...")
                
                # Download from HuggingFace Hub
                snapshot_download(
                    repo_id=model_name,
                    local_dir=str(model_path),
                    local_dir_use_symlinks=False
                )
                
                console.print(f"✅ Successfully installed {model_name}")
                return True
                
            except ImportError:
                console.print("❌ HuggingFace Hub not available. Please install with: pip install huggingface_hub")
                return False
            except Exception as e:
                console.print(f"❌ Failed to download {model_name}: {e}")
                return False
                
        except Exception as e:
            console.print(f"❌ Failed to install {model_name}: {e}")
            return False

    def uninstall_model(self, model_name: str) -> bool:
        """Uninstall a SuperOptiX model from MLX."""
        try:
            model_path = self.cache_dir / model_name.replace("/", "_")
            if model_path.exists():
                import shutil
                shutil.rmtree(model_path)
                return True
            return False
        except Exception:
            return False

    def get_model_info(self, model_name: str) -> Optional[SuperOptiXModelInfo]:
        """Get information about a specific SuperOptiX model."""
        try:
            # First check if it's installed
            installed_models = self.list_installed_models()
            for model in installed_models:
                if model.name == model_name:
                    return model
            
            # If not installed, check if it's available
            available_models = self.list_available_models()
            for model in available_models:
                if model.name == model_name:
                    return model
            
            return None
        except Exception:
            return None

    def test_model(self, model_name: str, prompt: str = "Hello, world!") -> Dict[str, Any]:
        """Test a SuperOptiX model with a simple prompt."""
        try:
            if not self.is_available():
                from rich.console import Console  # noqa: F401
                from rich.panel import Panel
                from rich.text import Text
                from rich.columns import Columns
                
                # Use the global console instance defined at the top of the module
                
                # Create colorful error message
                error_text = Text("❌ MLX is not available on this system", style="bold red")
                
                # Requirements section
                requirements = Text()
                requirements.append("🔧 MLX requires:\n", style="bold yellow")
                requirements.append("  • Apple Silicon (M1/M2/M3) with macOS\n", style="cyan")
                requirements.append("  • Python 3.9–3.12\n", style="cyan")
                requirements.append("  • The 'mlx' and 'mlx-lm' packages installed\n", style="cyan")
                
                # Installation instructions
                install_text = Text()
                install_text.append("🚀 To install MLX, run:\n", style="bold green")
                install_text.append("  pip install mlx mlx-lm\n", style="bright_white")
                install_text.append("  or (with uv):\n", style="bright_white")
                install_text.append("  uv pip install mlx mlx-lm\n", style="bright_white")
                install_text.append("  or (with conda):\n", style="bright_white")
                install_text.append("  conda install -c apple mlx mlx-lm\n", style="bright_white")
                
                # Next steps
                next_steps = Text()
                next_steps.append("📚 See https://github.com/ml-explore/mlx for more details\n", style="blue")
                next_steps.append("💡 After installation, try: super model install -b mlx <model_name>\n", style="bright_green")
                
                # Create panels
                error_panel = Panel(error_text, border_style="red", title="🍎 MLX Setup Required")
                req_panel = Panel(requirements, border_style="yellow", title="📋 Requirements")
                install_panel = Panel(install_text, border_style="green", title="⚡ Installation")
                next_panel = Panel(next_steps, border_style="blue", title="🎯 Next Steps")
                
                # Display in columns for better layout
                console.print()
                console.print(error_panel)
                console.print()
                console.print(Columns([req_panel, install_panel]))
                console.print()
                console.print(next_panel)
                console.print()
                
                return {
                    "success": False,
                    "error": "MLX is not available on this system",
                    "model": model_name,
                    "prompt": prompt,
                }
            
            # Import MLX tools
            import sys
            sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "mlx-lm-latest"))
            from mlx_lm import generate
            
            # Find model path
            model_path = self.cache_dir / model_name.replace("/", "_")
            if not model_path.exists():
                return {
                    "success": False,
                    "error": f"Model {model_name} not found locally",
                    "model": model_name,
                    "prompt": prompt,
                }
            
            start_time = datetime.now()
            
            # Generate response
            response = generate(str(model_path), prompt, max_tokens=50)
            
            end_time = datetime.now()
            
            return {
                "success": True,
                "response": response,
                "model": model_name,
                "prompt": prompt,
                "response_time": (end_time - start_time).total_seconds(),
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "model": model_name,
                "prompt": prompt,
            }

    def create_dspy_client(self, model_name: str, **kwargs):
        """Create a DSPy-compatible client for SuperOptiX MLX."""
        try:
            # Use the same pattern as Ollama - dspy.LM with custom_openai/ prefix
            # LiteLLM supports MLX through the custom_openai provider
            import sys
            sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "dspy-latest"))
            import dspy
            
            # Extract parameters and avoid conflicts
            temperature = kwargs.pop("temperature", 0.7)
            max_tokens = kwargs.pop("max_tokens", 2048)
            api_base = kwargs.pop("api_base", "http://localhost:8000")
            
            return dspy.LM(
                model=f"custom_openai/{model_name}",
                api_base=api_base,
                temperature=temperature,
                max_tokens=max_tokens,
                **kwargs
            )
            
        except ImportError as e:
            raise RuntimeError(f"Failed to import DSPy: {e}")
        except Exception as e:
            raise RuntimeError(f"Failed to create MLX DSPy client: {e}")

    def _infer_model_size(self, model_name: str) -> Optional[SuperOptiXModelSize]:
        """Infer model size from name."""
        name_lower = model_name.lower()
        
        if any(x in name_lower for x in ['1b', '1.3b', '1.5b']):
            return SuperOptiXModelSize.TINY
        elif any(x in name_lower for x in ['3b', '7b', '6.7b']):
            return SuperOptiXModelSize.SMALL
        elif any(x in name_lower for x in ['8b', '13b', '14b']):
            return SuperOptiXModelSize.MEDIUM
        elif any(x in name_lower for x in ['30b', '34b', '70b', '72b']):
            return SuperOptiXModelSize.LARGE
        
        return None

    def _infer_model_task(self, model_name: str) -> Optional[SuperOptiXModelTask]:
        """Infer model task from name."""
        name_lower = model_name.lower()
        
        if any(x in name_lower for x in ['code', 'coder']):
            return SuperOptiXModelTask.CODE
        elif any(x in name_lower for x in ['embed', 'embedding']):
            return SuperOptiXModelTask.EMBEDDING
        elif any(x in name_lower for x in ['vision', 'llava']):
            return SuperOptiXModelTask.VISION
        elif any(x in name_lower for x in ['qwen', 'reasoning']):
            return SuperOptiXModelTask.REASONING
        else:
            return SuperOptiXModelTask.CHAT

    def _extract_parameters(self, model_name: str) -> Optional[str]:
        """Extract parameter count from model name."""
        
        # Look for patterns like 1B, 3B, 7B, etc.
        match = re.search(r'(\d+(?:\.\d+)?[bm])', model_name.lower())
        if match:
            return match.group(1).upper()
        
        return None 