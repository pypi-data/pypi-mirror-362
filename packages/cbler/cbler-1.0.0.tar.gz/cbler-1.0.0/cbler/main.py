import typer
from concat import code, git  # add more as you extend
# from concat import py  # placeholder for future

app = typer.Typer(add_completion=False, no_args_is_help=True)

# Register language/model subcommands
app.add_typer(code.app, name="code")
app.add_typer(git.app, name="git")
# app.add_typer(py.app, name="py")  # placeholder for future

if __name__ == "__main__":
    app()
