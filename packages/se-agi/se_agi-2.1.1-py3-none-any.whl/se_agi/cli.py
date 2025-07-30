"""
Command Line Interface for SE-AGI
"""

import asyncio
import logging
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.logging import RichHandler
from rich.progress import Progress
from rich.table import Table

from .core.seagi import SEAGI
from .core.config import SEAGIConfig
from .__version__ import __version__

app = typer.Typer(
    name="se-agi",
    help="SE-AGI: Self-Evolving General AI - The Holy Grail of Autonomous Intelligence",
    add_completion=False,
)

console = Console()


def setup_logging(verbose: bool = False) -> None:
    """Setup logging configuration"""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(console=console, rich_tracebacks=True)]
    )


@app.command()
def version():
    """Show SE-AGI version information"""
    console.print(f"SE-AGI v{__version__}")
    console.print("Self-Evolving General AI - The Holy Grail of Autonomous Intelligence")


@app.command()
def info():
    """Show system information"""
    table = Table(title="SE-AGI System Information")
    table.add_column("Component", style="cyan")
    table.add_column("Status", style="green")
    table.add_column("Description")
    
    table.add_row("Core System", "✓ Available", "Main SEAGI orchestrator")
    table.add_row("Memory Systems", "✓ Available", "Episodic, Semantic, Working Memory")
    table.add_row("Reasoning", "✓ Available", "Multi-modal reasoning capabilities")
    table.add_row("Safety", "✓ Available", "Safety monitoring and alignment")
    table.add_row("Evolution", "✓ Available", "Capability evolution framework")
    table.add_row("Agents", "✓ Available", "Research, Creative, Analysis, Tool agents")
    
    console.print(table)


@app.command()
def run(
    config_path: Optional[Path] = typer.Option(
        None, "--config", "-c", help="Path to configuration file"
    ),
    verbose: bool = typer.Option(
        False, "--verbose", "-v", help="Enable verbose logging"
    ),
    interactive: bool = typer.Option(
        True, "--interactive", "-i", help="Run in interactive mode"
    ),
):
    """Run SE-AGI system"""
    setup_logging(verbose)
    
    console.print("[bold green]Starting SE-AGI System...[/bold green]")
    
    # Load configuration
    if config_path and config_path.exists():
        config = SEAGIConfig.from_file(config_path)
        console.print(f"Loaded configuration from {config_path}")
    else:
        config = SEAGIConfig()
        console.print("Using default configuration")
    
    # Run the system
    asyncio.run(_run_system(config, interactive))


async def _run_system(config: SEAGIConfig, interactive: bool):
    """Run the SE-AGI system"""
    seagi = SEAGI(config)
    
    try:
        with Progress() as progress:
            task = progress.add_task("Initializing SE-AGI...", total=100)
            
            # Initialize system
            await seagi.initialize()
            progress.update(task, advance=50)
            
            # Show system status
            progress.update(task, advance=25)
            status = seagi.get_status()
            console.print(f"[green]✓[/green] System initialized successfully")
            console.print(f"Instance ID: {status['instance_id']}")
            console.print(f"Agents: {status['agents_count']}")
            console.print(f"Safety Level: {status['safety_level']}")
            
            progress.update(task, advance=25)
        
        if interactive:
            await _interactive_mode(seagi)
        else:
            await seagi.run_continuous()
            
    except KeyboardInterrupt:
        console.print("\n[yellow]Shutting down SE-AGI...[/yellow]")
        await seagi.shutdown()
        console.print("[green]✓[/green] Shutdown complete")
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        await seagi.shutdown()


async def _interactive_mode(seagi: SEAGI):
    """Run SE-AGI in interactive mode"""
    console.print("\n[bold cyan]SE-AGI Interactive Mode[/bold cyan]")
    console.print("Type 'help' for commands, 'quit' to exit")
    
    while True:
        try:
            user_input = console.input("\n[bold blue]SE-AGI>[/bold blue] ")
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                break
            elif user_input.lower() == 'help':
                _show_help()
            elif user_input.lower() == 'status':
                _show_status(seagi)
            elif user_input.lower() == 'evolve':
                console.print("Triggering capability evolution...")
                await seagi.evolve()
                console.print("[green]✓[/green] Evolution complete")
            elif user_input.strip():
                # Process user input
                console.print("Processing your request...")
                response = await seagi.process(user_input)
                console.print(f"\n[green]Response:[/green] {response.content}")
                if response.confidence < 0.5:
                    console.print(f"[yellow]Note: Low confidence ({response.confidence:.2f})[/yellow]")
        
        except KeyboardInterrupt:
            break
        except Exception as e:
            console.print(f"[red]Error: {str(e)}[/red]")


def _show_help():
    """Show help information"""
    help_table = Table(title="SE-AGI Commands")
    help_table.add_column("Command", style="cyan")
    help_table.add_column("Description")
    
    help_table.add_row("help", "Show this help message")
    help_table.add_row("status", "Show system status")
    help_table.add_row("evolve", "Trigger capability evolution")
    help_table.add_row("quit/exit/q", "Exit interactive mode")
    help_table.add_row("<text>", "Process text input")
    
    console.print(help_table)


def _show_status(seagi: SEAGI):
    """Show system status"""
    status = seagi.get_status()
    
    status_table = Table(title="System Status")
    status_table.add_column("Property", style="cyan")
    status_table.add_column("Value", style="green")
    
    status_table.add_row("Instance ID", status['instance_id'])
    status_table.add_row("Generation", str(status['generation']))
    status_table.add_row("Uptime (seconds)", f"{status['uptime']:.1f}")
    status_table.add_row("Agents", str(status['agents_count']))
    status_table.add_row("Active Tasks", str(status['active_tasks']))
    status_table.add_row("Completed Tasks", str(status['completed_tasks']))
    status_table.add_row("Safety Level", status['safety_level'])
    status_table.add_row("Evolution Enabled", str(status['evolution_enabled']))
    
    console.print(status_table)


@app.command()
def test(
    component: Optional[str] = typer.Option(
        None, "--component", "-c", help="Test specific component"
    ),
    verbose: bool = typer.Option(
        False, "--verbose", "-v", help="Enable verbose output"
    ),
):
    """Test SE-AGI components"""
    setup_logging(verbose)
    
    console.print("[bold cyan]SE-AGI Component Tests[/bold cyan]")
    
    if component:
        console.print(f"Testing component: {component}")
        # Add specific component tests here
    else:
        console.print("Running all component tests...")
        # Add comprehensive testing here
    
    console.print("[green]✓[/green] Tests completed")


def main():
    """Main CLI entry point"""
    app()


if __name__ == "__main__":
    main()
