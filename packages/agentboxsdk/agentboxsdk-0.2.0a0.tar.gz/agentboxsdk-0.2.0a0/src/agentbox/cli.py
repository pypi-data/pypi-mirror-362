import typer
import asyncio
from dotenv import load_dotenv
from pathlib import Path
from importlib.metadata import version, PackageNotFoundError

from agentbox import Box, __version__
from agentbox.settings import Settings
from agentbox.agents.reactive import ReactiveAgent

try:
    __version__: str = version("agentboxsdk")
except PackageNotFoundError:
    __version__ = "0.0.0.dev0"

load_dotenv()

app = typer.Typer(no_args_is_help=True, help="AgentBox SDK CLI", rich_markup_mode=None)


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    version: bool = typer.Option(False, "--version", help="Show version and exit"),
):
    """AgentBox SDK CLI"""
    if version:
        typer.echo(f"AgentBox SDK v{__version__}")
        raise typer.Exit()

    if ctx.invoked_subcommand is None:
        typer.echo(ctx.get_help())


# ─────────────── init ─────────────── #
@app.command()
def init(
    path: Path = typer.Option(
        Settings.locate_yaml() or Path(".agentbox.yaml"),
        help="Where to create the YAML (defaults cwd)",
    ),
):
    """Generate a starter .agentbox.yaml."""
    if path.exists():
        typer.secho(f"[!] {path} already exists -- aborting.", fg=typer.colors.RED)
        raise typer.Exit(1)
    Settings().save(path)
    typer.secho(f"✔ Wrote {path}", fg=typer.colors.GREEN)


# ─────────────── ask ─────────────── #
@app.command("ask")
def ask_command(
    prompt: str = typer.Argument(..., help="Your question"),
    engine: str | None = typer.Option(None, "-e", "--engine", help="Override engine"),
    model: str | None = typer.Option(None, "-m", "--model", help="Override model"),
    stream: bool = typer.Option(
        False, "-s", "--stream", "-ns", "--no-stream", help="Stream the response"
    ),
):
    """Ask the configured model a question."""
    settings = Settings.load()
    if engine:
        settings.engine = engine
    if model:
        settings.model = model

    try:
        box = Box.from_settings(settings)
    except ValueError as exc:
        typer.secho(str(exc), fg="red")
        raise typer.Exit(1)

    if stream:
        for chunk in box.stream(prompt):
            typer.echo(chunk, nl=False)
        typer.echo()
    else:
        answer = asyncio.run(box.async_ask(prompt))
        typer.secho(answer, fg=typer.colors.GREEN)


@app.command("run")
def run_agent_cmd(
    prompt: str = typer.Argument(None, help="Prompt for ReactiveAgent"),
    code: str | None = typer.Option(None, "--code", help="Raw Python expression"),
):
    """Run the built-in ReactiveAgent or execute code directly."""
    if code:
        prompt = f"```python\n{code}\n```"
    box = Box.from_settings()
    agent = ReactiveAgent()
    typer.echo(box.run_agent(agent, prompt))


@app.command("search")
def search_cmd(query: str = typer.Argument(...)):
    """Quick DuckDuckGo search via SearchTool."""
    from agentbox.tools import get_tool

    Search = get_tool("search")
    typer.echo(Search().run(query=query))


def run():
    app()
