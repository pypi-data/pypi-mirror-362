import typer
from rich.console import Console
from rich.table import Table
from rich import box
from rich.panel import Panel
import subprocess
import pathlib

app = typer.Typer(help="Show pretty git commit log.")


def get_git_log(path, n):
    try:
        cmd = [
            "git",
            "-C",
            str(path),
            "log",
            f"-n{n}",
            "--pretty=format:%C(auto)%h%Creset|%C(yellow)%d%Creset|%s|%C(dim)%cr%Creset|%an",
            "--decorate=short",
            "--date=relative",
        ]
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT).decode("utf-8")
        lines = [l for l in output.splitlines() if l.strip()]
        return lines
    except subprocess.CalledProcessError as e:
        return [f"[red]Error running git: {e.output.decode('utf-8')}[/red]"]
    except FileNotFoundError:
        return ["[red]Git is not installed or not on PATH.[/red]"]


def get_git_branches(path):
    try:
        output = (
            subprocess.check_output(
                ["git", "-C", str(path), "branch", "--show-current"],
                stderr=subprocess.STDOUT,
            )
            .decode("utf-8")
            .strip()
        )
        return output if output else None
    except Exception:
        return None


@app.command()
def log(
    directory: str = typer.Argument(".", help="Directory to search for git repo"),
    num: int = typer.Argument(10, help="Number of commits to show"),
):
    """Pretty print recent git commits, with branch info if available."""
    path = pathlib.Path(directory).resolve()
    console = Console()

    # Show branch if it exists
    branch = get_git_branches(path)
    if branch:
        console.print(
            Panel(
                f"[bold green]On branch:[/bold green] [yellow]{branch}[/yellow]",
                box=box.ROUNDED,
            )
        )

    # Show log table
    lines = get_git_log(path, num)
    table = Table(
        show_header=True,
        header_style="bold magenta",
        box=box.SIMPLE_HEAVY,
        padding=(0, 1),
    )
    table.add_column("Hash", style="cyan", no_wrap=True)
    table.add_column("Ref", style="yellow", no_wrap=True)
    table.add_column("Message", style="white")
    table.add_column("When", style="dim", no_wrap=True)
    table.add_column("Who", style="green", no_wrap=True)

    for line in lines:
        if line.startswith("[red]"):
            console.print(line)
            return
        parts = line.split("|", maxsplit=4)
        if len(parts) == 5:
            table.add_row(*[p.strip() for p in parts])
        else:
            table.add_row(*parts, *[""] * (5 - len(parts)))
    console.print(table)
