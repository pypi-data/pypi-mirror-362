import typer
from rich import print
import os
import sys
import subprocess

packageFileName = "requirements.txt"
preset = "windows" if os.name == "nt" else "default"
app = typer.Typer(no_args_is_help=True)

@app.command()
def about():
    print("[bold cyan]Sage by Viuv Labs[/bold cyan]: A unified build and dependency system for C/C++")
    print("[faint white]Use '--help' to explore commands[/faint white]")

@app.command()
def compile():
    if not os.path.isfile("CMakeLists.txt"):
        print("[bold red]Missing CMakeLists.txt[/bold red]")
        return
    
    build_dir = f"build/{preset}"
    if not os.path.isdir(build_dir):
        result = subprocess.run(["cmake", "--preset", preset])
        if result.returncode != 0:
            print("[bold red]CMake configuration failed[/bold red]")
            return
    
    subprocess.run(["cmake", "--build", build_dir, "--parallel"])

@app.command()
def run(args: list[str]):
    if not args:
        print("[bold red]Specify at least one app to run[/bold red]")
        return

    for arg in args:
        path_direct = f"build/{preset}/{arg}"
        path_nested = f"{path_direct}/{arg}"
        if os.path.isfile(path_direct):
            subprocess.run([path_direct])
        elif os.path.isfile(path_nested):
            subprocess.run([path_nested])
        else:
            print(f"[bold red]Executable '{arg}' not found[/bold red]")

@app.command()
def install(
    package: str = typer.Option(None, "--package", "-p", help="Package name to install"),
    version: str = typer.Option(None, "--version", "-v", help="Optional package version")
):
    req_path = f"packages/{packageFileName}"

    if not package:
        if os.path.isfile(req_path):
            subprocess.run(["conan", "install", req_path, "--output-folder", "packages/install", "--build=missing"])
        else:
            print(f"[bold red]Missing {req_path}[/bold red]")
        return
    req_dir=os.path.dirname(req_path)
    os.makedirs(req_dir,exist_ok=True)
    
    if not os.path.isfile(req_path):
        with open(req_path, "w") as f:
            f.write("[requires]\n[generators]\nCMakeDeps\nCMakeToolchain\n")

    if not version:
        print(f"[bold green]No version provided for {package}. Fetching latest...[/bold green]")
        search = subprocess.run(["conan", "search", package], capture_output=True, text=True)
        if search.returncode != 0:
            print(f"[bold red]Conan search failed for {package}[/bold red]")
            return
        lines = search.stdout.strip().splitlines()
        version = lines[-1].split("/")[1] if lines else ""

    if not version:
        print(f"[bold red]No available versions found for {package}[/bold red]")
        return

    full_package = f"{package}/{version}"
    print(f"[bold yellow]Installing: {full_package}[/bold yellow]")

    with open(req_path, "r") as f:
        lines = f.readlines()

    if full_package + "\n" in lines:
        print(f"[bold yellow]{full_package} is already listed[/bold yellow]")
        return

    for i, line in enumerate(lines):
        if line.strip() == "[requires]":
            lines.insert(i + 1, full_package + "\n")
            break

    with open(req_path, "w") as f:
        f.writelines(lines)

    subprocess.run(["conan", "install", req_path, "--output-folder", "packages/install", "--build=missing"])

@app.command()
def doctor():
    print("[bold blue]Diagnostics are in progress... stay tuned![/bold blue]")