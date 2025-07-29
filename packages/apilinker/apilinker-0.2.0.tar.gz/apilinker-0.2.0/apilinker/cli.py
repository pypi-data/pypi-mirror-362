"""
Command Line Interface for ApiLinker.
"""

import os
import sys
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from apilinker import ApiLinker, __version__
from apilinker.core.logger import setup_logger

# Create Typer app
app = typer.Typer(
    name="apilinker",
    help="A universal bridge to connect, map, and automate data transfer between any two REST APIs.",
    add_completion=False,
)

# Create console for rich output
console = Console()


@app.command()
def version() -> None:
    """Show the version of ApiLinker."""
    console.print(f"ApiLinker v{__version__}")


@app.command()
def sync(
    config: Path = typer.Option(
        ...,
        "--config",
        "-c",
        help="Path to configuration YAML file",
        exists=True,
        dir_okay=False,
        readable=True,
    ),
    log_level: str = typer.Option(
        "INFO",
        "--log-level",
        "-l",
        help="Logging level (DEBUG, INFO, WARNING, ERROR)",
    ),
    log_file: Optional[Path] = typer.Option(
        None,
        "--log-file",
        "-f",
        help="Path to log file",
    ),
    dry_run: bool = typer.Option(
        False,
        "--dry-run",
        "-d",
        help="Perform a dry run without making changes",
    ),
    source_endpoint: Optional[str] = typer.Option(
        None,
        "--source-endpoint",
        "-s",
        help="Source endpoint to use (overrides config)",
    ),
    target_endpoint: Optional[str] = typer.Option(
        None,
        "--target-endpoint",
        "-t",
        help="Target endpoint to use (overrides config)",
    ),
) -> None:
    """
    Sync data between source and target APIs based on configuration.
    """
    logger = setup_logger(log_level, log_file)
    logger.info(f"ApiLinker v{__version__} starting sync")
    
    try:
        # Initialize ApiLinker with config
        linker = ApiLinker(
            config_path=str(config),
            log_level=log_level,
            log_file=str(log_file) if log_file else None,
        )
        
        # If dry run, just report what would happen
        if dry_run:
            console.print("[bold yellow]DRY RUN MODE[/bold yellow] - No data will be transferred")
            source_url = linker.source.base_url if linker.source is not None else 'Not configured'
            target_url = linker.target.base_url if linker.target is not None else 'Not configured'
            console.print(f"Source: {source_url}")
            console.print(f"Target: {target_url}")
            mappings = linker.mapper.get_mappings()
            
            if mappings:
                table = Table(title="Field Mappings")
                table.add_column("Source Endpoint", style="cyan")
                table.add_column("Target Endpoint", style="green")
                table.add_column("Field Count", style="magenta")
                
                for mapping in mappings:
                    table.add_row(
                        mapping["source"],
                        mapping["target"],
                        str(len(mapping["fields"]))
                    )
                
                console.print(table)
            else:
                console.print("[yellow]No mappings configured[/yellow]")
                
            return
        
        # Execute the sync
        result = linker.sync(
            source_endpoint=source_endpoint,
            target_endpoint=target_endpoint,
        )
        
        # Report results
        if result.success:
            console.print(f"[bold green]Sync completed successfully![/bold green]")
            console.print(f"Transferred [bold]{result.count}[/bold] items")
            
            if result.details:
                console.print("\n[bold]Details:[/bold]")
                for key, value in result.details.items():
                    console.print(f"  {key}: {value}")
        else:
            console.print(f"[bold red]Sync failed![/bold red]")
            for error in result.errors:
                console.print(f"[red]Error: {error}[/red]")
    
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")
        logger.exception("Error during sync operation")
        sys.exit(1)


@app.command()
def run(
    config: Path = typer.Option(
        ...,
        "--config",
        "-c",
        help="Path to configuration YAML file",
        exists=True,
        dir_okay=False,
        readable=True,
    ),
    log_level: str = typer.Option(
        "INFO",
        "--log-level",
        "-l",
        help="Logging level (DEBUG, INFO, WARNING, ERROR)",
    ),
    log_file: Optional[Path] = typer.Option(
        None,
        "--log-file",
        "-f",
        help="Path to log file",
    ),
) -> None:
    """
    Run scheduled syncs based on configuration.
    """
    logger = setup_logger(log_level, log_file)
    logger.info(f"ApiLinker v{__version__} starting scheduler")
    
    try:
        # Initialize ApiLinker with config
        linker = ApiLinker(
            config_path=str(config),
            log_level=log_level,
            log_file=str(log_file) if log_file else None,
        )
        
        # Show schedule info
        schedule_info = linker.scheduler.get_schedule_info()
        console.print(f"[bold]Schedule:[/bold] {schedule_info}")
        
        # Start scheduled sync
        console.print("Starting scheduled sync. Press CTRL+C to stop.")
        linker.start_scheduled_sync()
        
    except KeyboardInterrupt:
        console.print("\n[yellow]Stopping scheduled sync...[/yellow]")
        linker.stop_scheduled_sync()
        console.print("[green]Stopped[/green]")
    
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")
        logger.exception("Error during scheduled sync")
        sys.exit(1)


@app.command()
def validate(
    config: Path = typer.Option(
        ...,
        "--config",
        "-c",
        help="Path to configuration YAML file",
        exists=True,
        dir_okay=False,
        readable=True,
    ),
) -> None:
    """
    Validate configuration file without performing any actions.
    """
    try:
        # Initialize ApiLinker with config (will validate the config)
        ApiLinker(config_path=str(config))
        
        console.print(f"[bold green]Configuration is valid![/bold green]")
        console.print(f"Configuration file: {config}")
    
    except Exception as e:
        console.print(f"[bold red]Configuration error:[/bold red] {str(e)}")
        sys.exit(1)


@app.command()
def init(
    output: Path = typer.Option(
        "config.yaml",
        "--output",
        "-o",
        help="Path to output configuration file",
    ),
    force: bool = typer.Option(
        False,
        "--force",
        "-f",
        help="Overwrite existing file if it exists",
    ),
) -> None:
    """
    Initialize a new configuration file with a template.
    """
    # Check if output file exists
    if output.exists() and not force:
        console.print(f"[bold red]Error:[/bold red] File {output} already exists. Use --force to overwrite.")
        sys.exit(1)
    
    # Create template config
    template = """# ApiLinker Configuration

source:
  type: rest
  base_url: https://api.example.com/v1
  auth:
    type: bearer
    token: ${SOURCE_API_TOKEN}
  endpoints:
    list_items:
      path: /items
      method: GET
      params:
        updated_since: "{{last_sync}}"

target:
  type: rest
  base_url: https://api.destination.com/v2
  auth:
    type: api_key
    header: X-API-Key
    key: ${TARGET_API_KEY}
  endpoints:
    create_item:
      path: /items
      method: POST

mapping:
  - source: list_items
    target: create_item
    fields:
      - source: id
        target: external_id
      - source: name
        target: title
      - source: description
        target: body.content
      - source: created_at
        target: metadata.created
        transform: iso_to_timestamp

# Optional schedule configuration
schedule:
  type: interval
  minutes: 60

logging:
  level: INFO
  file: apilinker.log
"""
    
    # Write template to file
    with open(output, "w") as f:
        f.write(template)
    
    console.print(f"[bold green]Template configuration created:[/bold green] {output}")
    console.print("Edit this file with your API details before running apilinker sync.")


if __name__ == "__main__":
    app()
