import typer
from cbler import code, git

app = typer.Typer(add_completion=False, no_args_is_help=True)

# Register language/model subcommands
app.add_typer(code.app, name="code")
app.add_typer(git.app, name="git")

if __name__ == "__main__":
    app()
