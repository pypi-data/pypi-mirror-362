"""
Command-line interface for Prompt Gear.
"""
import json
import sys
from pathlib import Path
from typing import Optional, Dict, Any

import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm

from . import PromptManager, PromptNotFoundError, PromptAlreadyExistsError
from .schema import PromptTemplate

app = typer.Typer(
    name="promptgear",
    help="YAML-powered prompt manager with multi-backend support",
    rich_markup_mode="rich"
)
console = Console()


@app.command()
def create(
    name: str = typer.Argument(..., help="Prompt name"),
    version: str = typer.Option("v1", "--version", "-v", help="Prompt version"),
    system: Optional[str] = typer.Option(None, "--system", "-s", help="System prompt"),
    user: Optional[str] = typer.Option(None, "--user", "-u", help="User prompt"),
    config: Optional[str] = typer.Option(None, "--config", "-c", help="Config as JSON string"),
    interactive: bool = typer.Option(False, "--interactive", "-i", help="Interactive mode"),
    overwrite: bool = typer.Option(False, "--overwrite", help="Overwrite existing prompt"),
):
    """Create a new prompt template."""
    try:
        pm = PromptManager()
        
        if interactive:
            # Interactive mode
            name = name or Prompt.ask("Prompt name")
            version = version or Prompt.ask("Version", default="v1")
            system = system or Prompt.ask("System prompt")
            user = user or Prompt.ask("User prompt")
            
            config_str = Prompt.ask("Config (JSON, optional)", default="")
            if config_str.strip():
                try:
                    config_dict = json.loads(config_str)
                except json.JSONDecodeError:
                    console.print("[red]Invalid JSON format for config[/red]")
                    sys.exit(1)
            else:
                config_dict = {}
        else:
            # Non-interactive mode
            if not system:
                console.print("[red]System prompt is required[/red]")
                sys.exit(1)
            if not user:
                console.print("[red]User prompt is required[/red]")
                sys.exit(1)
            
            config_dict = {}
            if config:
                try:
                    config_dict = json.loads(config)
                except json.JSONDecodeError:
                    console.print("[red]Invalid JSON format for config[/red]")
                    sys.exit(1)
        
        # Create prompt
        prompt = pm.create_prompt(
            name=name,
            version=version,
            system_prompt=system,
            user_prompt=user,
            config=config_dict,
            overwrite=overwrite
        )
        
        console.print(f"[green]✓[/green] Created prompt [bold]{name}:{version}[/bold]")
        _display_prompt(prompt)
        
    except PromptAlreadyExistsError as e:
        console.print(f"[red]Error:[/red] {e}")
        console.print("Use --overwrite to overwrite existing prompt")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)


@app.command()
def get(
    name: str = typer.Argument(..., help="Prompt name"),
    version: Optional[str] = typer.Option(None, "--version", "-v", help="Prompt version (if not specified, gets latest version)"),
    format: str = typer.Option("rich", "--format", "-f", help="Output format (rich, json, yaml)")
):
    """Get a prompt template."""
    try:
        pm = PromptManager()
        prompt = pm.get_prompt(name, version)
        
        if format == "json":
            console.print(prompt.json(indent=2))
        elif format == "yaml":
            import yaml
            console.print(yaml.dump(prompt.dict(), default_flow_style=False))
        else:
            _display_prompt(prompt)
            
    except PromptNotFoundError as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)


@app.command()
def list(
    name: Optional[str] = typer.Option(None, "--name", "-n", help="Filter by prompt name"),
    format: str = typer.Option("table", "--format", "-f", help="Output format (table, json)")
):
    """List prompt templates."""
    try:
        pm = PromptManager()
        prompts = pm.list_prompts(name)
        
        if not prompts:
            console.print("[yellow]No prompts found[/yellow]")
            return
        
        if format == "json":
            console.print(json.dumps([p.dict() for p in prompts], indent=2))
        else:
            table = Table(title="Prompt Templates")
            table.add_column("Name", style="cyan")
            table.add_column("Version", style="magenta")
            table.add_column("System Prompt", style="green", max_width=40)
            table.add_column("User Prompt", style="blue", max_width=40)
            table.add_column("Config", style="yellow")
            
            for prompt in prompts:
                config_str = json.dumps(prompt.config) if prompt.config else "{}"
                table.add_row(
                    prompt.name,
                    prompt.version,
                    prompt.system_prompt[:100] + "..." if len(prompt.system_prompt) > 100 else prompt.system_prompt,
                    prompt.user_prompt[:100] + "..." if len(prompt.user_prompt) > 100 else prompt.user_prompt,
                    config_str
                )
            
            console.print(table)
            
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)


@app.command()
def delete(
    name: str = typer.Argument(..., help="Prompt name"),
    version: str = typer.Option("v1", "--version", "-v", help="Prompt version"),
    yes: bool = typer.Option(False, "--yes", "-y", help="Skip confirmation")
):
    """Delete a prompt template."""
    try:
        pm = PromptManager()
        
        if not pm.prompt_exists(name, version):
            console.print(f"[red]Error:[/red] Prompt {name}:{version} not found")
            sys.exit(1)
        
        if not yes:
            if not Confirm.ask(f"Delete prompt {name}:{version}?"):
                console.print("Cancelled")
                return
        
        pm.delete_prompt(name, version)
        console.print(f"[green]✓[/green] Deleted prompt [bold]{name}:{version}[/bold]")
        
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)


@app.command()
def versions(
    name: str = typer.Argument(..., help="Prompt name")
):
    """List versions of a prompt."""
    try:
        pm = PromptManager()
        versions = pm.list_versions(name)
        
        if not versions:
            console.print(f"[yellow]No versions found for prompt '{name}'[/yellow]")
            return
        
        console.print(f"[bold]Versions for '{name}':[/bold]")
        for version in versions:
            console.print(f"  • {version}")
            
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)


@app.command()
def init(
    backend: str = typer.Option("filesystem", "--backend", "-b", help="Backend type (filesystem, sqlite, postgres)"),
    force: bool = typer.Option(False, "--force", help="Force initialization")
):
    """Initialize Prompt Gear in current directory."""
    try:
        env_path = Path(".env")
        
        if env_path.exists() and not force:
            console.print("[yellow]Warning:[/yellow] .env file already exists")
            if not Confirm.ask("Overwrite existing .env file?"):
                console.print("Cancelled")
                return
        
        # Create .env file
        env_content = f"""# Prompt Gear Configuration
PROMPT_GEAR_BACKEND={backend}
PROMPT_GEAR_PROMPT_DIR=./prompts
PROMPT_GEAR_DB_URL=sqlite:///prompts.db
# PROMPT_GEAR_DB_URL=postgresql://user:pass@localhost/prompts

# Development settings
PROMPT_GEAR_DEBUG=false
"""
        
        with open(env_path, 'w') as f:
            f.write(env_content)
        
        # Initialize backend
        pm = PromptManager()
        pm.backend.initialize()
        
        console.print(f"[green]✓[/green] Initialized Prompt Gear with {backend} backend")
        console.print(f"[green]✓[/green] Created .env configuration file")
        
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)


@app.command()
def status():
    """Show Prompt Gear status and backend information."""
    try:
        pm = PromptManager()
        
        # Get basic info
        backend_type = pm.config.backend
        console.print(f"[bold]Prompt Gear Status[/bold]")
        console.print(f"Backend: [cyan]{backend_type}[/cyan]")
        
        # Get backend-specific info
        if backend_type == "filesystem":
            console.print(f"Prompts directory: [green]{pm.config.prompt_dir}[/green]")
            prompts = pm.list_prompts()
            console.print(f"Total prompts: [yellow]{len(prompts)}[/yellow]")
            
            # Count unique names
            unique_names = len(set(p.name for p in prompts))
            console.print(f"Unique prompt names: [yellow]{unique_names}[/yellow]")
        
        elif backend_type == "sqlite":
            # Try to get stats if backend supports it
            try:
                if hasattr(pm.backend, 'get_stats'):
                    stats = pm.backend.get_stats()
                    console.print(f"Database: [green]{stats['database_path']}[/green]")
                    console.print(f"Total prompts: [yellow]{stats['total_prompts']}[/yellow]")
                    console.print(f"Unique prompt names: [yellow]{stats['unique_names']}[/yellow]")
                else:
                    console.print(f"Database URL: [green]{pm.config.db_url}[/green]")
                    prompts = pm.list_prompts()
                    console.print(f"Total prompts: [yellow]{len(prompts)}[/yellow]")
            except Exception as e:
                console.print(f"[red]Error getting stats:[/red] {e}")
        
        elif backend_type == "postgres":
            # Try to get stats if backend supports it
            try:
                if hasattr(pm.backend, 'get_stats'):
                    stats = pm.backend.get_stats()
                    console.print(f"Database URL: [green]{stats['database_url']}[/green]")
                    console.print(f"Database version: [green]{stats['database_version']}[/green]")
                    console.print(f"Total prompts: [yellow]{stats['total_prompts']}[/yellow]")
                    console.print(f"Unique prompt names: [yellow]{stats['unique_names']}[/yellow]")
                    console.print(f"Connection pool size: [blue]{stats['pool_size']}[/blue]")
                    console.print(f"Max connections: [blue]{stats['max_connections']}[/blue]")
                    
                    # Show config usage statistics
                    if stats.get('config_stats'):
                        console.print(f"\n[bold]Config usage:[/bold]")
                        for config_stat in stats['config_stats'][:5]:
                            console.print(f"  • {config_stat['key']}: {config_stat['count']} prompts")
                else:
                    console.print(f"Database URL: [green]{pm.config.db_url}[/green]")
                    prompts = pm.list_prompts()
                    console.print(f"Total prompts: [yellow]{len(prompts)}[/yellow]")
            except Exception as e:
                console.print(f"[red]Error getting stats:[/red] {e}")
        
        else:
            console.print(f"Database URL: [green]{pm.config.db_url}[/green]")
            prompts = pm.list_prompts()
            console.print(f"Total prompts: [yellow]{len(prompts)}[/yellow]")
        
        # Show recent prompts
        prompts = pm.list_prompts()
        if prompts:
            console.print(f"\n[bold]Recent prompts:[/bold]")
            for prompt in prompts[:5]:  # Show first 5
                console.print(f"  • {prompt.name}:{prompt.version}")
            
            if len(prompts) > 5:
                console.print(f"  ... and {len(prompts) - 5} more")
        else:
            console.print(f"\n[yellow]No prompts found[/yellow]")
            
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)


@app.command()
def search(
    query: str = typer.Argument(..., help="Search query"),
    field: str = typer.Option("all", "--field", "-f", help="Search field (all, name, system_prompt, user_prompt)"),
    format: str = typer.Option("table", "--format", help="Output format (table, json)")
):
    """Search prompt templates."""
    try:
        pm = PromptManager()
        
        # Check if backend supports search
        if not hasattr(pm.backend, 'search_prompts'):
            console.print("[red]Search is not supported by the current backend[/red]")
            sys.exit(1)
        
        prompts = pm.backend.search_prompts(query, field)
        
        if not prompts:
            console.print(f"[yellow]No prompts found for query '{query}'[/yellow]")
            return
        
        if format == "json":
            console.print(json.dumps([p.dict() for p in prompts], indent=2))
        else:
            table = Table(title=f"Search Results for '{query}'")
            table.add_column("Name", style="cyan")
            table.add_column("Version", style="magenta")
            table.add_column("System Prompt", style="green", max_width=40)
            table.add_column("User Prompt", style="blue", max_width=40)
            
            for prompt in prompts:
                table.add_row(
                    prompt.name,
                    prompt.version,
                    prompt.system_prompt[:100] + "..." if len(prompt.system_prompt) > 100 else prompt.system_prompt,
                    prompt.user_prompt[:100] + "..." if len(prompt.user_prompt) > 100 else prompt.user_prompt
                )
            
            console.print(table)
            
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)


@app.command()
def find_by_config(
    config_json: str = typer.Argument(..., help="JSON config to search for"),
    format: str = typer.Option("table", "--format", help="Output format (table, json)")
):
    """Find prompts by configuration parameters."""
    try:
        pm = PromptManager()
        
        # Check if backend supports config queries
        if not hasattr(pm.backend, 'get_prompts_by_config'):
            console.print("[red]Config queries are not supported by the current backend[/red]")
            sys.exit(1)
        
        try:
            config_query = json.loads(config_json)
        except json.JSONDecodeError:
            console.print("[red]Invalid JSON format for config[/red]")
            sys.exit(1)
        
        prompts = pm.backend.get_prompts_by_config(config_query)
        
        if not prompts:
            console.print(f"[yellow]No prompts found with config {config_json}[/yellow]")
            return
        
        if format == "json":
            console.print(json.dumps([p.dict() for p in prompts], indent=2))
        else:
            table = Table(title=f"Prompts with config {config_json}")
            table.add_column("Name", style="cyan")
            table.add_column("Version", style="magenta")
            table.add_column("Config", style="yellow")
            
            for prompt in prompts:
                table.add_row(
                    prompt.name,
                    prompt.version,
                    json.dumps(prompt.config, indent=2) if prompt.config else "{}"
                )
            
            console.print(table)
            
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)


@app.command()
def test_connection():
    """Test database connection (for database backends)."""
    try:
        pm = PromptManager()
        
        # Check if backend supports connection testing
        if hasattr(pm.backend, 'get_connection'):
            console.print("[bold]Testing database connection...[/bold]")
            
            # Test connection
            conn = pm.backend.get_connection()
            if conn:
                console.print("[green]✓ Database connection successful[/green]")
                pm.backend.put_connection(conn)
                
                # Get database info
                if hasattr(pm.backend, 'get_stats'):
                    stats = pm.backend.get_stats()
                    console.print(f"Database: {stats.get('database_version', 'Unknown')}")
                    console.print(f"Pool size: {stats.get('pool_size', 'N/A')}")
                    console.print(f"Max connections: {stats.get('max_connections', 'N/A')}")
            else:
                console.print("[red]✗ Failed to connect to database[/red]")
                sys.exit(1)
        else:
            console.print("[yellow]Connection testing not supported by current backend[/yellow]")
            
    except Exception as e:
        console.print(f"[red]Connection test failed:[/red] {e}")
        sys.exit(1)


def _display_prompt(prompt: PromptTemplate):
    """Display a prompt in rich format."""
    panel_content = f"""[bold cyan]Name:[/bold cyan] {prompt.name}
[bold magenta]Version:[/bold magenta] {prompt.version}

[bold green]System Prompt:[/bold green]
{prompt.system_prompt}

[bold blue]User Prompt:[/bold blue]
{prompt.user_prompt}

[bold yellow]Config:[/bold yellow]
{json.dumps(prompt.config, indent=2) if prompt.config else '{}'}"""
    
    console.print(Panel(panel_content, title="Prompt Template", expand=False))


if __name__ == "__main__":
    app()
