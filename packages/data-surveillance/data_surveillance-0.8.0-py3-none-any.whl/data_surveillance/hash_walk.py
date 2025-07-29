import json
import os
from pathlib import Path
import hashlib
from collections import OrderedDict
from .bootstrap import SPY_RESULTS_DIR
from data_surveillance.bootstrap import HASH_OUTPUT_FILE_NAME


def hash_content(path: Path) -> dict:
    _tree = dict()
    for root, _, files in os.walk(path):
        root_path = Path(root)
        for file in files:
            if file.startswith("."):
                continue
            file_path = root_path / file
            _tree[str(f"{root_path.name}__{file}")] = {
                "sha": str(
                    hashlib.sha256(file_path.read_bytes()).digest(),
                ),
                "path": str(file_path),
            }
    return {k: _tree[k] for k in sorted(_tree)}


def save(path: Path, tree: dict) -> None:
    path.joinpath(HASH_OUTPUT_FILE_NAME).write_text(json.dumps(tree))


def hash_walk(path: Path) -> None:
    tree = hash_content(path=path)
    save(path, tree)
