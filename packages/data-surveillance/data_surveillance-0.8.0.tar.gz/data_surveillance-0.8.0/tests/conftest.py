import os
import shutil
from pathlib import Path
from collections.abc import Generator

from pytest import fixture


@fixture
def path() -> Generator[Path]:
    path = Path(os.environ["_SPY_RESULTS_DIR"])
    path.mkdir(exist_ok=True)
    yield path

    shutil.rmtree(path)
