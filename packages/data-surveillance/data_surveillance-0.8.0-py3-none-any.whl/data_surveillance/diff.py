import json
from pathlib import Path

import pandas as pd
from pandas.testing import assert_frame_equal

from data_surveillance.bootstrap import HASH_OUTPUT_FILE_NAME


def find_miss(v1: dict, v2: dict) -> set[str]:
    diff = set(v1) - set(v2)
    for file in diff:
        print(f"miss - {file}")

    return diff


def find_diff(v1: dict, v2: dict) -> set[str]:
    intrsection = set(v1).intersection(set(v2))
    diff = set()

    for file in intrsection:
        if not file.endswith(".csv") and v1[file]["sha"] != v2[file]["sha"]:
            print(f"diff - {file}")
            diff.add(file)
        if file.endswith(".csv") and v1[file]["sha"] != v2[file]["sha"]:
            df_base = pd.read_csv(v1[file]["path"], index_col=0)
            df_test = pd.read_csv(v1[file]["path"], index_col=0)
            if not assert_frame_equal(df_base, df_test):
                print(f"diff - {file}")

    return diff


def diff(base: Path, test: Path) -> None:
    if base == test:
        raise ValueError("base and test paths can not be the same")

    if not all([base.exists(), test.exists()]):
        raise ValueError("base and test paths have to exist")

    if base.is_dir() and base.joinpath(HASH_OUTPUT_FILE_NAME).exists():
        base = base.joinpath(HASH_OUTPUT_FILE_NAME)
    else:
        raise ValueError("base file not found")

    if test.is_dir() and test.joinpath(HASH_OUTPUT_FILE_NAME).exists():
        test = test.joinpath(HASH_OUTPUT_FILE_NAME)
    else:
        raise ValueError("test file not found")

    base_encoded: dict = json.loads(base.read_text())
    test_encoded: dict = json.loads(test.read_text())

    print("Base vs Test - miss")
    find_miss(base_encoded, test_encoded)
    print("-" * 10)
    print("Test vs Base - miss")
    find_miss(test_encoded, base_encoded)
    print("-" * 10)
    print("Diff")
    find_diff(base_encoded, test_encoded)
    print("-" * 10)
