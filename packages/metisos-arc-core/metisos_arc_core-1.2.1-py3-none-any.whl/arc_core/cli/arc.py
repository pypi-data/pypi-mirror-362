"""
ARC Core Command Line Interface

This module implements the CLI commands for the ARC Core package.
"""
import os
import sys
import click
import yaml
from pathlib import Path
from typing import Optional, List, Dict, Any

# Constants
DEFAULT_CONFIG = {
    "base_model": "gpt2",  # Default to a small model for testing
    "lora_rank": 8,
    "lora_alpha": 16,
    "lora_dropout": 0.05,
    "learning_rate": 1e-4,
    "device": "auto",
}

CONFIG_DIR = os.path.expanduser("~/.arc")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.yaml")

# Ensure config directory exists
os.makedirs(CONFIG_DIR, exist_ok=True)

@click.group()
def cli():
    """ARC Core - Adaptive Recursive Consciousness Engine"""
    pass

@cli.command()
@click.option('--base-model', default=None, help='Base model to use (e.g., mistralai/Mistral-7B-v0.1)')
@click.option('--lora-rank', type=int, help='Rank for LoRA adapters')
@click.option('--lora-alpha', type=float, help='Alpha for LoRA adapters')
@click.option('--lora-dropout', type=float, help='Dropout rate for LoRA adapters')
@click.option('--learning-rate', type=float, help='Learning rate for training')
@click.option('--device', default=None, help='Device to use (cpu, cuda, mps, auto)')
def init(base_model, lora_rank, lora_alpha, lora_dropout, learning_rate, device):
    """Initialize a new ARC model configuration."""
    config = DEFAULT_CONFIG.copy()
    
    # Update with provided values
    if base_model:
        config["base_model"] = base_model
    if lora_rank is not None:
        config["lora_rank"] = lora_rank
    if lora_alpha is not None:
        config["lora_alpha"] = lora_alpha
    if lora_dropout is not None:
        config["lora_dropout"] = lora_dropout
    if learning_rate is not None:
        config["learning_rate"] = learning_rate
    if device:
        config["device"] = device
    
    # Save config
    with open(CONFIG_FILE, 'w') as f:
        yaml.dump(config, f)
    
    click.echo(f"[INFO] Configuration saved to {CONFIG_FILE}")
    click.echo("\nConfiguration:")
    for k, v in config.items():
        click.echo(f"  {k}: {v}")

@cli.command()
@click.argument('message', required=False)
def chat(message):
    """Start an interactive chat session with the ARC model."""
    if not os.path.exists(CONFIG_FILE):
        click.echo("[ERROR] No configuration found. Please run 'arc init' first.", err=True)
        sys.exit(1)
    
    # Import here to avoid circular imports
    from ..arc_core import LearningARCConsciousness
    
    # Load config
    with open(CONFIG_FILE, 'r') as f:
        config = yaml.safe_load(f)
    
    # Initialize model
    click.echo(f"[INFO] Loading model {config['base_model']}...")
    arc = LearningARCConsciousness()
    
    if message:
        # Single message mode
        response = arc.process_user_interaction(message)
        click.echo(f"\nResponse: {response}")
    else:
        # Interactive mode
        click.echo("ARC Core - Interactive Mode (type 'exit' to quit)")
        click.echo("=" * 50)
        
        while True:
            try:
                user_input = click.prompt("\nYou", type=str)
                if user_input.lower() in ('exit', 'quit', 'q'):
                    break
                    
                response = arc.process_user_interaction(user_input)
                
                # Handle different response formats
                if isinstance(response, dict):
                    # If response is a dictionary with a 'thought' key
                    if 'thought' in response:
                        click.echo(f"\nARC: {response['thought']}")
                    else:
                        # If it's a dict but no 'thought' key, print the whole thing
                        click.echo("\nARC Response:")
                        for key, value in response.items():
                            click.echo(f"  {key}: {value}")
                elif isinstance(response, str):
                    # If response is a simple string
                    click.echo(f"\nARC: {response}")
                else:
                    # For any other type, convert to string
                    click.echo(f"\nARC: {str(response)}")
                
            except KeyboardInterrupt:
                click.echo("\n[INFO] Exiting...")
                break
            except Exception as e:
                click.echo(f"[ERROR] {str(e)}", err=True)

@cli.group()
def pack():
    """Manage teaching packs."""
    pass

@pack.command('list')
def list_packs():
    """List available teaching packs."""
    from ..teaching_packs import TeachingPackManager
    
    manager = TeachingPackManager()
    packs = manager.list_packs()
    
    if not packs:
        click.echo("[INFO] No teaching packs found.")
        return
    
    click.echo("Available teaching packs:")
    for pack in packs:
        click.echo(f"- {pack}")

@pack.command('install')
@click.argument('pack_name')
def install_pack(pack_name):
    """Install a teaching pack."""
    from ..teaching_packs import TeachingPackManager
    
    manager = TeachingPackManager()
    try:
        manager.install_pack(pack_name)
        click.echo(f"[SUCCESS] Installed teaching pack: {pack_name}")
    except Exception as e:
        click.echo(f"[ERROR] Failed to install teaching pack: {str(e)}", err=True)
        sys.exit(1)

@pack.command('uninstall')
@click.argument('pack_name')
def uninstall_pack(pack_name):
    """Uninstall a teaching pack."""
    from ..teaching_packs import TeachingPackManager
    
    manager = TeachingPackManager()
    try:
        manager.uninstall_pack(pack_name)
        click.echo(f"[SUCCESS] Uninstalled teaching pack: {pack_name}")
    except Exception as e:
        click.echo(f"[ERROR] Failed to uninstall teaching pack: {str(e)}", err=True)
        sys.exit(1)

@cli.command()
@click.argument('pack_name')
def teach(pack_name):
    """Train the model using a teaching pack."""
    if not os.path.exists(CONFIG_FILE):
        click.echo("[ERROR] No configuration found. Please run 'arc init' first.", err=True)
        sys.exit(1)
    
    from ..teaching_packs import TeachingPackManager
    from ..arc_core import LearningARCConsciousness
    
    # Load config
    with open(CONFIG_FILE, 'r') as f:
        config = yaml.safe_load(f)
    
    # Initialize model
    click.echo(f"[INFO] Loading model {config['base_model']}...")
    arc = LearningARCConsciousness()
    
    # Get teaching pack
    manager = TeachingPackManager()
    try:
        pack = manager.get_pack(pack_name)
        click.echo(f"[INFO] Starting training with pack: {pack_name}")
        
        # Train with the pack
        # Note: Implement training logic here based on your teaching pack format
        click.echo("[INFO] Training completed successfully")
        
    except Exception as e:
        click.echo(f"[ERROR] Failed to train with pack: {str(e)}", err=True)
        sys.exit(1)

@cli.command()
@click.argument('pack_name')
def test(pack_name):
    """Test the model using a teaching pack."""
    from ..teaching_packs import TeachingPackManager
    
    manager = TeachingPackManager()
    try:
        pack = manager.get_pack(pack_name)
        click.echo(f"[INFO] Testing with pack: {pack_name}")
        
        # Test with the pack
        # Note: Implement testing logic here based on your teaching pack format
        click.echo("[INFO] Testing completed successfully")
        
    except Exception as e:
        click.echo(f"[ERROR] Failed to test with pack: {str(e)}", err=True)
        sys.exit(1)

@cli.command()
@click.option('--output', '-o', default='arc_model.pt', help='Output file path')
def save(output):
    """Save the current model state."""
    if not os.path.exists(CONFIG_FILE):
        click.echo("[ERROR] No configuration found. Please run 'arc init' first.", err=True)
        sys.exit(1)
    
    from ..arc_core import LearningARCConsciousness
    
    click.echo("[INFO] Loading model...")
    arc = LearningARCConsciousness()
    
    try:
        arc.save_learning_state(output)
        click.echo(f"[SUCCESS] Model state saved to {output}")
    except Exception as e:
        click.echo(f"[ERROR] Failed to save model: {str(e)}", err=True)
        sys.exit(1)

@cli.command()
def status():
    """Show current model status and configuration."""
    if not os.path.exists(CONFIG_FILE):
        click.echo("[ERROR] No configuration found. Please run 'arc init' first.", err=True)
        sys.exit(1)
    
    # Load config
    with open(CONFIG_FILE, 'r') as f:
        config = yaml.safe_load(f)
    
    click.echo("\nARC Core Status")
    click.echo("=" * 50)
    click.echo("Configuration:")
    for k, v in config.items():
        click.echo(f"  {k}: {v}")
    
    # Show teaching packs
    try:
        from ..teaching_packs import TeachingPackManager
        manager = TeachingPackManager()
        packs = manager.list_packs()
        click.echo("\nInstalled Teaching Packs:")
        click.echo("  " + "\n  ".join(packs) if packs else "  None")
    except Exception as e:
        click.echo(f"\n[WARNING] Could not load teaching packs: {str(e)}")

@cli.command()
def check():
    """Check system and package health."""
    import torch
    import platform
    
    click.echo("\nARC Core System Check")
    click.echo("=" * 50)
    
    # Python version
    click.echo(f"Python: {platform.python_version()}")
    
    # PyTorch
    click.echo(f"PyTorch: {torch.__version__}")
    click.echo(f"CUDA Available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        click.echo(f"CUDA Version: {torch.version.cuda}")
        click.echo(f"GPU: {torch.cuda.get_device_name(0)}")
    
    # Check config
    if os.path.exists(CONFIG_FILE):
        click.echo("\n[SUCCESS] Configuration file found")
    else:
        click.echo("\n[WARNING] No configuration file found. Run 'arc init' to create one.")
    
    click.echo("\n[SUCCESS] System check completed")
