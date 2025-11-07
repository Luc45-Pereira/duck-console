"""
Command-line interface for duck-console
"""
import typer
from duck_console.web import main as web_main

app = typer.Typer()

@app.command()
def web():
    """Start the web console interface"""
    web_main()

@app.command()
def shell():
    """Start an interactive DuckDB shell"""
    # TODO: Implement interactive shell
    typer.echo("Interactive shell not yet implemented")