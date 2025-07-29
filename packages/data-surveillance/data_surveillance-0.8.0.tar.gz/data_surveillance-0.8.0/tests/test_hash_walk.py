import hashlib
from pathlib import Path
from data_surveillance.hash_walk import hash_content
import pytest


def test_hash_walk_one_file(path: Path) -> None:
    # given
    value = b"test"
    file_name = "file.txt"

    # when
    path.joinpath(file_name).write_bytes(value)
    result: dict = hash_content(path)
    # then

    assert len(result) == 1
    given_key, given_value = result.popitem()
    assert file_name in given_key
    assert given_value == str(hashlib.sha256(value).digest())


def test_hash_walk_many_files(path: Path) -> None:
    # given
    value1 = b"test1"
    value2 = b"test2"
    file_name1 = "file1.txt"
    file_name2 = "file2.txt"

    # when
    path.joinpath(file_name1).write_bytes(value1)
    path.joinpath(file_name2).write_bytes(value2)
    result: dict = hash_content(path)
    # then

    assert len(result) == 2

    given_key, given_value = result.popitem()
    assert file_name2 in given_key
    assert given_value == str(hashlib.sha256(value2).digest())

    given_key, given_value = result.popitem()
    assert file_name1 in given_key
    assert given_value == str(hashlib.sha256(value1).digest())
