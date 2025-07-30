import typer
from rich.console import Console
from rich.table import Table
from rich import box
from rich.panel import Panel
import subprocess
import pathlib

app = typer.Typer(help="Show pretty git commit log.")


console = Console()


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


@app.command()
def diff(
    directory: str = typer.Argument(".", help="Directory to search for git repo"),
    staged: bool = typer.Option(
        False, "--staged", "-s", help="Show staged diff (default: unstaged)"
    ),
):
    """
    Show files changed in git diff (unstaged by default, use --staged for staged changes).
    """
    path = pathlib.Path(directory).resolve()

    branch = get_git_branches(path)
    if branch:
        console.print(
            Panel(
                f"[bold green]On branch:[/bold green] [yellow]{branch}[/yellow]",
                title="Branch",
            )
        )

    # Get diff with --numstat (shows added/removed per file)
    cmd = ["git", "-C", str(path), "diff", "--numstat"]
    if staged:
        cmd.append("--cached")
    try:
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT).decode("utf-8")
    except subprocess.CalledProcessError as e:
        console.print(f"[red]Error: {e.output.decode('utf-8')}[/red]")
        return

    table = Table(
        show_header=True,
        header_style="bold magenta",
        box=box.SIMPLE_HEAVY,
        title="Changed Files",
    )
    table.add_column("Added", style="green", justify="right")
    table.add_column("Removed", style="red", justify="right")
    table.add_column("File", style="cyan")

    if not output.strip():
        table.add_row("-", "-", "[dim]No changes[/dim]")
    else:
        for line in output.strip().splitlines():
            added, removed, filename = line.split("\t", 2)
            table.add_row(added, removed, filename)

    console.print(table)


@app.command()
def tree(
    directory: str = typer.Argument(".", help="Directory to search for git repo"),
    num: int = typer.Option(20, "--num", "-n", help="Number of commits to show"),
):
    """
    Show a simple git branch/commit graph for the last N commits.
    """
    path = pathlib.Path(directory).resolve()
    branch = get_git_branches(path)
    if branch:
        console.print(
            Panel(
                f"[bold green]On branch:[/bold green] [yellow]{branch}[/yellow]",
                title="Branch",
            )
        )

    cmd = [
        "git",
        "-C",
        str(path),
        "log",
        "--graph",
        "--oneline",
        "--decorate",
        f"-n{num}",
        "--color=never",
    ]
    try:
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT).decode("utf-8")
    except subprocess.CalledProcessError as e:
        console.print(f"[red]Error: {e.output.decode('utf-8')}[/red]")
        return

    # Print as a rich Panel (Rich can't really parse the ascii graph, but it can color the text)
    console.print(
        Panel(
            f"[white]{output}[/white]",
            title=f"Git Graph (last {num} commits)",
            subtitle="[dim]Use --num/-n to change depth[/dim]",
            style="cyan",
        )
    )
