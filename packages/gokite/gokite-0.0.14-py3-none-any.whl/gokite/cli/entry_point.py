import typer


entrypoint_cli_typer = typer.Typer(
    no_args_is_help=True,
    add_completion=False,
    rich_markup_mode="markdown",
    help="",
)


def version_callback(value: bool):
    if value:
        from .. import __version__

        typer.echo(f"gokite client version: {__version__}")
        raise typer.Exit()


@entrypoint_cli_typer.callback()
def gokite(
    ctx: typer.Context,
    version: bool = typer.Option(None, "--version", callback=version_callback),
):
    pass


entrypoint_cli = typer.main.get_command(entrypoint_cli_typer)
entrypoint_cli.list_commands(None)  # type: ignore


if __name__ == "__main__":
    # this module is only called from tests, otherwise the parent package __main__.py is used as the entrypoint
    entrypoint_cli()
