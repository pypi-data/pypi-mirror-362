import os
import pathlib
import typer
import pyperclip
import re
from rich.console import Console
from rich.tree import Tree
from rich.panel import Panel
from rich.table import Table
from rich import box
import subprocess

console = Console()


def report_results(
    copied: list[str], skipped: list[str], base_path: pathlib.Path, operation="Copied"
):
    """Pretty-print tree of copied files and a summary panel."""
    # Tree
    tree = Tree(
        f"[bold green]{operation} files from [yellow]{base_path}[/yellow][/bold green]"
    )
    for rel_path in sorted(copied):
        _add_path_to_tree(tree, rel_path)
    if copied:
        console.print(tree)
    else:
        console.print("[red]No files matched the filters. Nothing copied.[/red]")
    # Summary
    table = Table(show_header=True, header_style="bold magenta", box=box.ROUNDED)
    table.add_column("Result", style="cyan", justify="center")
    table.add_column("Count", style="yellow", justify="right")
    table.add_row("[green]Copied[/green]", str(len(copied)))
    table.add_row("[red]Skipped[/red]", str(len(skipped)))
    console.print(Panel(table, title="[bold]Summary[/bold]", subtitle=":rocket:"))


def _add_path_to_tree(tree: Tree, rel_path: str):
    """Add a relative file path to a Rich Tree, creating directories as needed."""
    parts = rel_path.replace("\\", "/").split("/")
    branch = tree
    for part in parts[:-1]:
        # find or add sub-branch for each dir
        existing = None
        for child in branch.children:
            if isinstance(child, Tree) and child.label == part:
                existing = child
                break
        if existing:
            branch = existing
        else:
            branch = branch.add(part)
    branch.add(f"[bold white]{parts[-1]}[/bold white]")


app = typer.Typer(help="Concatenate source code files by language.")


## helpers
def get_git_repo_root(path):
    try:
        cmd = ["git", "-C", str(path), "rev-parse", "--show-toplevel"]
        result = subprocess.check_output(cmd, stderr=subprocess.DEVNULL)
        return pathlib.Path(result.decode("utf-8").strip())
    except Exception:
        return None


def get_git_changed_files(repo_root, staged=False):
    cmd = ["git", "-C", str(repo_root), "diff", "--name-only"]
    if staged:
        cmd.append("--cached")
    try:
        result = subprocess.check_output(cmd, stderr=subprocess.DEVNULL)
        files = [f.replace("\\", "/") for f in result.decode("utf-8").splitlines()]
        return set(files)
    except subprocess.CalledProcessError:
        return set()


def parent_folder_name(rel_path: str) -> str:
    return pathlib.Path(rel_path).parent.name


def split_patterns(values: list[str]) -> list[str]:
    result = []
    for v in values or []:
        result.extend(v.strip().split())
    return [p for p in result if p]


def any_match(patterns, value, use_regex, match_type="start"):
    for pat in patterns:
        try:
            if use_regex:
                if match_type == "start":
                    if re.match(pat, value):
                        return True
                elif match_type == "end":
                    if re.search(f"{pat}$", value):
                        return True
                else:
                    if re.search(pat, value):
                        return True
            else:
                if match_type == "start":
                    if value.startswith(pat):
                        return True
                elif match_type == "end":
                    if value.endswith(pat):
                        return True
                else:
                    if pat in value:
                        return True
        except re.error as e:
            print(f"[regex error] pattern '{pat}': {e}")
            continue

    return False


###############
# GML SECTION #
###############

SCRIPT_EXTENSIONS = [".gml"]
OBJECT_EXTENSIONS = [".yy"]


def extract_gml_code(filepath: str) -> str:
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


def extract_yy_code(filepath: str) -> str:
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = f.read()
        object_name = pathlib.Path(filepath).stem
        matches = re.findall(r'"code"\s*:\s*"([^"]+)"', data)
        return (
            "\n\n".join(
                f"// Extracted Script {i + 1}:\n{code}"
                for i, code in enumerate(matches)
            )
            if matches
            else f"// Object: {object_name} (No code found)"
        )
    except Exception as e:
        return f"// ⚠️ Error reading {filepath}: {e}"


@app.command("gml")
def gml(
    path: str = typer.Argument(".", help="Path to GameMaker project"),
    prefix: list[str] = typer.Option(
        None, "--prefix", help="Only include files with these prefixes"
    ),
    not_prefix: list[str] = typer.Option(
        None, "--not-prefix", help="Exclude files with these prefixes"
    ),
    suffix: list[str] = typer.Option(
        None, "--suffix", help="Only include files with these suffixes"
    ),
    not_suffix: list[str] = typer.Option(
        None, "--not-suffix", help="Exclude files with these suffixes"
    ),
    contains: list[str] = typer.Option(
        None, "--contains", help="Filename contains (regex ok)"
    ),
    not_contains: list[str] = typer.Option(
        None, "--not-contains", help="Filename does NOT contain (regex ok)"
    ),
    path_contains: list[str] = typer.Option(
        None, "--path-contains", help="Relative path contains (regex ok)"
    ),
    not_path_contains: list[str] = typer.Option(
        None, "--not-path-contains", help="Relative path does NOT contain (regex ok)"
    ),
    parent_contains: list[str] = typer.Option(
        None, "--parent-contains", help="Direct parent folder matches (regex ok)"
    ),
    not_parent_contains: list[str] = typer.Option(
        None,
        "--not-parent-contains",
        help="Direct parent folder does NOT match (regex ok)",
    ),
    regex: bool = typer.Option(
        True, help="Use regex for all filters (default: true)", show_default=False
    ),
    git_diff: bool = typer.Option(
        False,
        "--git-diff",
        "--changed",
        help="Only include files seen as changed by git",
    ),
):
    """Concatenate .gml and .yy code and copy to clipboard."""

    copied_files = []
    skipped_files = []

    script_output = []
    base_path = pathlib.Path(path).resolve()

    repo_root = get_git_repo_root(base_path) if git_diff else None

    pf = split_patterns(prefix)
    npf = split_patterns(not_prefix)
    sf = split_patterns(suffix)
    nsf = split_patterns(not_suffix)
    cf = split_patterns(contains)
    ncf = split_patterns(not_contains)
    pcf = split_patterns(path_contains)
    npcf = split_patterns(not_path_contains)
    parcf = split_patterns(parent_contains)
    nparcf = split_patterns(not_parent_contains)

    changed_files = set()
    if git_diff and repo_root:
        changed_files = get_git_changed_files(repo_root)

    for root, _, files in os.walk(base_path):
        for file in files:
            file_path = os.path.join(root, file)
            rel_path = os.path.relpath(file_path, base_path)
            parent_name = parent_folder_name(rel_path)

            if git_diff and rel_path.replace("\\", "/") not in changed_files:
                continue

            # Positive filters
            if pf and not any_match(pf, file, regex, "start"):
                skipped_files.append(rel_path)
                continue

            if sf and not any_match(sf, file, regex, "end"):
                skipped_files.append(rel_path)
                continue

            if cf and not any_match(cf, file, regex, "any"):
                skipped_files.append(rel_path)
                continue

            if pcf and not any_match(pcf, rel_path, regex, "any"):
                skipped_files.append(rel_path)
                continue

            if parcf and not any_match(parcf, parent_name, regex, "any"):
                skipped_files.append(rel_path)
                continue

            # Negative filters
            if npf and any_match(npf, file, regex, "start"):
                skipped_files.append(rel_path)
                continue

            if nsf and any_match(nsf, file, regex, "end"):
                skipped_files.append(rel_path)
                continue

            if ncf and any_match(ncf, file, regex, "any"):
                skipped_files.append(rel_path)
                continue

            if npcf and any_match(npcf, rel_path, regex, "any"):
                skipped_files.append(rel_path)
                continue

            if nparcf and any_match(nparcf, parent_name, regex, "any"):
                skipped_files.append(rel_path)
                continue

            if file.endswith(tuple(SCRIPT_EXTENSIONS)):
                script_output.append(
                    f"// Script: {rel_path}\n" + extract_gml_code(file_path)
                )
                copied_files.append(rel_path)

            elif file.endswith(tuple(OBJECT_EXTENSIONS)):
                script_output.append(
                    f"// Object: {rel_path}\n" + extract_yy_code(file_path)
                )
                copied_files.append(rel_path)

    final = "\n\n".join(script_output)
    pyperclip.copy(final)
    report_results(copied_files, skipped_files, base_path, operation="Copied")


###############
# PYTHON SECTION #
###############

SKIP_DIRS = {"venv", ".venv", "__pycache__", ".git"}


@app.command("py")
def py(
    path: str = typer.Argument(".", help="Path to Python project"),
    prefix: list[str] = typer.Option(
        None,
        "--prefix",
        help="Only include files with these prefixes",
        show_default=False,
    ),
    not_prefix: list[str] = typer.Option(
        None,
        "--not-prefix",
        help="Exclude files with these prefixes",
        show_default=False,
    ),
    suffix: list[str] = typer.Option(
        [".py", ".pyc"],
        "--suffix",
        help="Only include files with these suffixes",
        show_default=False,
    ),
    not_suffix: list[str] = typer.Option(
        None,
        "--not-suffix",
        help="Exclude files with these suffixes",
        show_default=False,
    ),
    contains: list[str] = typer.Option(
        None,
        "--contains",
        help="Only include files whose name matches ANY of these regex patterns",
        show_default=False,
    ),
    not_contains: list[str] = typer.Option(
        None,
        "--not-contains",
        help="Exclude files whose name matches ANY of these regex patterns",
        show_default=False,
    ),
    regex: bool = typer.Option(
        True, help="Use regex for all filters (default: true)", show_default=False
    ),
    git_diff: bool = typer.Option(
        False,
        "--git-diff",
        "--changed",
        help="Only include files seen as changed by git",
    ),
):
    """Concatenate python files and copy to clipboard."""
    copied_files = []
    skipped_files = []
    script_output = []
    base_path = pathlib.Path(path).resolve()
    pf = split_patterns(prefix)
    npf = split_patterns(not_prefix)
    sf = split_patterns(suffix)
    nsf = split_patterns(not_suffix)
    cf = split_patterns(contains)
    ncf = split_patterns(not_contains)

    repo_root = get_git_repo_root(base_path) if git_diff else None

    changed_files = set()
    if git_diff and repo_root:
        changed_files = get_git_changed_files(repo_root)

    for root, dirs, files in os.walk(base_path):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for file in files:
            file_path = os.path.join(root, file)
            rel_path = os.path.relpath(file_path, base_path)

            if git_diff and rel_path.replace("\\", "/") not in changed_files:
                continue

            # Inclusive filters
            if pf and not any_match(pf, file, regex, "start"):
                skipped_files.append(rel_path)
                continue

            if sf and not any_match(sf, file, regex, "end"):
                skipped_files.append(rel_path)
                continue

            if cf and not any_match(cf, file, regex, "any"):
                skipped_files.append(rel_path)
                continue

            # Exclusive filters
            if npf and any_match(npf, file, regex, "start"):
                skipped_files.append(rel_path)
                continue

            if nsf and any_match(nsf, file, regex, "end"):
                skipped_files.append(rel_path)
                continue

            if ncf and any_match(ncf, file, regex, "any"):
                skipped_files.append(rel_path)
                continue

            file_path = os.path.join(root, file)
            rel_path = os.path.relpath(file_path, base_path)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    code = f.read()
                script_output.append(f"# File: {rel_path}\n{code}")
                copied_files.append(rel_path)

            except Exception as e:
                script_output.append(f"# ⚠️ Error reading {rel_path}: {e}")
    final = "\n\n".join(script_output)
    pyperclip.copy(final)
    report_results(copied_files, skipped_files, base_path, operation="Copied")
