import typer
from rich import print

app = typer.Typer()

@app.command()
def about():
    print("[bold cyan]Sage: A Unified Project and Package Management System for C/C++ by viuvlabs.[/bold cyan]")

def main():
    app()

if __name__ == "__main__":
    main()
