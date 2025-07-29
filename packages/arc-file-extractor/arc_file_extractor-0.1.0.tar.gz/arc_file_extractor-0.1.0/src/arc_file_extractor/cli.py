"""Console script for arc_file_extractor."""

import sys
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from .arc_file_extractor import ArcFileExtractor
from . import utils

app = typer.Typer(
    name="arc",
    help="Arc File Extractor - A unified CLI for file extraction and compression on UNIX systems.",
    no_args_is_help=True
)
console = Console()


@app.command("x", help="Extract a file to a directory with the same name")
def extract(
    file: str = typer.Argument(..., help="Path to the file to extract"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose output"),
    force: bool = typer.Option(False, "--force", "-f", help="Force extraction, overwrite existing files without asking")
):
    """Extract a file to a directory with the same name."""
    if not utils.validate_file_path(file):
        console.print(f"[red][!] File not found or not readable: {file}[/red]")
        raise typer.Exit(1)
    
    if verbose:
        file_size = utils.get_file_size(file)
        console.print(f"[blue]Extracting file: {file} ({file_size})[/blue]")
    
    extractor = ArcFileExtractor()
    result = extractor.extract(file, force=force)
    
    if result == 0:
        output_dir = Path(file).stem
        # Remove .tar from compound extensions
        if file.lower().endswith(('.tar.gz', '.tar.bz2', '.tar.xz')):
            output_dir = output_dir.replace('.tar', '')
        
        console.print(f"[green]✓ Successfully extracted to: {output_dir}/[/green]")
    else:
        console.print("[red][!] Extraction failed[/red]")
        raise typer.Exit(1)


@app.command("c", help="Compress a file or directory")
def compress(
    source: str = typer.Argument(..., help="Path to the file or directory to compress"),
    output: Optional[str] = typer.Option(None, "--output", "-o", help="Output file path (defaults to source.zip)"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose output")
):
    """Compress a file or directory."""
    if not Path(source).exists():
        console.print(f"[red][!] Source not found: {source}[/red]")
        raise typer.Exit(1)
    
    if output is None:
        output = f"{source}.zip"
    
    if verbose:
        if Path(source).is_file():
            source_size = utils.get_file_size(source)
            console.print(f"[blue]Compressing file: {source} ({source_size})[/blue]")
        else:
            console.print(f"[blue]Compressing directory: {source}/[/blue]")
        console.print(f"[blue]Output: {output}[/blue]")
    
    extractor = ArcFileExtractor()
    result = extractor.compress(source, output)
    
    if result == 0:
        output_size = utils.get_file_size(output)
        console.print(f"[green]✓ Successfully compressed to: {output} ({output_size})[/green]")
    else:
        console.print("[red][!] Compression failed[/red]")
        raise typer.Exit(1)


@app.command("list", help="List supported file formats")
def list_formats():
    """List supported file formats for extraction and compression."""
    formats = utils.get_supported_formats()
    
    table = Table(title="Supported File Formats", show_header=True, header_style="bold magenta")
    table.add_column("Operation", style="dim", width=12)
    table.add_column("Formats", style="cyan")
    
    table.add_row("Extract", ", ".join(formats["extract"]))
    table.add_row("Compress", ", ".join(formats["compress"]))
    
    console.print(table)


@app.command("check", help="Check system dependencies")
def check_dependencies():
    """Check if required external tools are installed."""
    missing = utils.check_dependencies()
    
    if not missing:
        console.print("[green]✓ All required dependencies are installed[/green]")
    else:
        console.print("[red][!] Missing dependencies:[/red]")
        for tool in missing:
            console.print(f"  • {tool}")
        console.print("\n[yellow]Install missing tools using your package manager[/yellow]")
        raise typer.Exit(1)


def main():
    """Main entry point for the CLI."""
    app()


if __name__ == "__main__":
    main()
