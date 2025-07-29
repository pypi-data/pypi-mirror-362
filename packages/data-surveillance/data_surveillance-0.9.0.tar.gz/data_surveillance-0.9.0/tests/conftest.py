import os
import shutil
from pathlib import Path
from collections.abc import Generator

from pytest import fixture


def get_all_genereated_files(path: Path) -> list[Path]:
    return sorted(
        [
            Path(root).joinpath(file)
            for (root, _, files) in os.walk(path, topdown=False)
            for file in files
            if not file.startswith(".")
        ]
    )


@fixture
def path() -> Generator[Path]:
    path = Path(os.environ["_SPY_RESULTS_DIR"])
    path.mkdir(exist_ok=True)
    yield path

    shutil.rmtree(path)
