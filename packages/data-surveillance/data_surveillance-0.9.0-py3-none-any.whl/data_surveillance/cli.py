from pathlib import Path
import click
from data_surveillance import hash_walk
from data_surveillance import diff as _diff


@click.group()
def cli():
    pass


@cli.command()
@click.argument(
    "path",
    type=click.Path(
        exists=True,
        file_okay=False,
        readable=True,
        path_type=Path,
    ),
)
def walk(path: Path):
    hash_walk(Path(path))


@cli.command()
@click.argument(
    "base",
    type=click.Path(
        exists=True,
        file_okay=False,
        readable=True,
        path_type=Path,
    ),
)
@click.argument(
    "test",
    type=click.Path(
        exists=True,
        file_okay=False,
        readable=True,
        path_type=Path,
    ),
)
def diff(base: Path, test: Path):
    _diff(base, test)
