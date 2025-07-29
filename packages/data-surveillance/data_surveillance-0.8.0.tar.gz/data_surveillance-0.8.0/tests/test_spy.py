import json
import os
from pathlib import Path
from typing import Any
from data_surveillance.spy import spy
import pytest
import pandas as pd
import os


def get_all_genereated_files(path: Path) -> list[Path]:
    return sorted(
        [
            Path(root).joinpath(file)
            for (root, _, files) in os.walk(path, topdown=False)
            for file in files
            if not file.startswith(".")
        ]
    )


def test_spy_in_one_func(path: Path):
    # given
    value = 1

    @spy
    def calc(value: int):
        pass

    # when
    calc(value=value)

    # then
    files = get_all_genereated_files(path=path)
    assert len(files) == 1, "File wasn't created"


def test_spy_in_two_func(path: Path):
    # given
    value = 1

    @spy
    def calc(value: int):
        pass

    # when
    calc(value=value)
    calc(value=value)

    # then
    files = get_all_genereated_files(path=path)
    assert len(files) == 2


def test_spy_in_out_one_func(path: Path) -> None:
    # given
    value = 1

    @spy
    def calc(value: int):
        return value * 10

    # when
    calc(value=value)

    # then
    files = get_all_genereated_files(path=path)
    assert len(files) == 2, "Files weren't created"


def test_spy_in_out_many_func(path: Path) -> None:
    # given
    value = 1

    @spy
    def calc(value: int):
        return value * 10

    # when
    calc(value=value)
    calc(value=value)

    # then
    files = get_all_genereated_files(path=path)
    assert len(files) == 4, "Files weren't created"


def test_spy_in_many_one_func(path: Path):
    # given
    value = 1

    @spy
    def calc(value: int, value1: int, value2: int):
        pass

    # when
    calc(value=value, value1=value, value2=value)

    # then
    files = get_all_genereated_files(path=path)
    assert len(files) == 3, "Files weren't created"


def test_spy_in_many_out_many_one_func(path: Path):
    # given
    value = 1

    @spy
    def calc(value: int, value1: int, value2: int):
        return (value, value1, value2)

    # when
    calc(value=value, value1=value, value2=value)

    # then
    files = get_all_genereated_files(path=path)
    assert len(files) == 6, "Files weren't created"


def test_spy_in_one_int_one_func(path: Path):
    # given
    _int = 1

    @spy
    def calc(_i: int):
        pass

    # when
    calc(_i=_int)

    # then
    files = get_all_genereated_files(path=path)
    assert str(_int) in files[0].read_text()


def test_spy_in_one_str_one_func(path: Path):
    # given
    value: str = "test"

    @spy
    def calc(value: str):
        pass

    # when
    calc(value=value)

    # then
    files = get_all_genereated_files(path=path)
    assert str(value) in files[0].read_text()


def test_spy_in_one_tuple_one_func(path: Path):
    # given
    value = (1, "2")

    @spy
    def calc(value):
        pass

    # when
    calc(value=value)

    # then
    files = get_all_genereated_files(path=path)
    assert list(value) == json.loads(files[0].read_text())


def test_spy_in_one_list_func(path: Path):
    # given
    value = [1, "2"]

    @spy
    def calc(value):
        pass

    # when
    calc(value=value)

    # then
    files = get_all_genereated_files(path=path)
    assert value == json.loads(files[0].read_text())


def test_spy_in_one_dict_one_func(path: Path):
    # given
    value = {"one": 1, "two": "2"}

    @spy
    def calc(value):
        pass

    # when
    calc(value=value)

    # then
    files = get_all_genereated_files(path=path)
    assert value == json.loads(files[0].read_text())


def test_spy_in_one_dataframe_one_func(path: Path) -> None:
    # given
    value = pd.DataFrame(
        {
            "col_1": [1, 2, 3],
            "col_2": [11, 22, 33],
        },
    )

    @spy
    def calc(value):
        pass

    # when
    calc(value=value)
    # then
    files = get_all_genereated_files(path=path)
    pd.testing.assert_frame_equal(value, pd.read_csv(files[0], index_col=0))


def test_spy_in_one_dataframe_one_func(path: Path) -> None:
    # given
    value = pd.DataFrame(
        {
            "col_2": [11, 33, 22],
            "col_1": [1, 3, 2],
        },
    )

    @spy
    def calc(value):
        pass

    # when
    calc(value=value)
    # then
    value_ordordered = pd.DataFrame(
        {
            "col_1": [1, 2, 3],
            "col_2": [11, 22, 33],
        },
    )
    files = get_all_genereated_files(path=path)
    pd.testing.assert_frame_equal(value_ordordered, pd.read_csv(files[0], index_col=0))


def test_spy_out_one_dataframe_one_func(path: Path) -> None:
    # given
    value = pd.DataFrame(
        {
            "col_1": [1, 2, 3],
            "col_2": [11, 22, 33],
        },
    )

    @spy
    def calc():
        return value

    # when
    calc()
    # then
    files = get_all_genereated_files(path=path)
    pd.testing.assert_frame_equal(value, pd.read_csv(files[0], index_col=0))


def test_spy_in_one_list_of_dataframes_one_func(path: Path) -> None:
    # given
    df1 = pd.DataFrame(
        {
            "col_1": [1, 2, 3],
            "col_2": [11, 22, 33],
        },
    )

    df2 = pd.DataFrame(
        {
            "col_2": [1, 2, 3],
            "col_3": [11, 22, 33],
        },
    )

    @spy
    def calc(value: list[pd.DataFrame]):
        pass

    # when
    calc(value=[df1, df2])
    # then
    files = get_all_genereated_files(path=path)
    pd.testing.assert_frame_equal(df1, pd.read_csv(files[0], index_col=0))
    pd.testing.assert_frame_equal(df2, pd.read_csv(files[1], index_col=0))


def test_spy_out_one_list_of_dataframes_one_func(path: Path) -> None:
    # given
    df1 = pd.DataFrame(
        {
            "col_1": [1, 2, 3],
            "col_2": [11, 22, 33],
        },
    )

    df2 = pd.DataFrame(
        {
            "col_2": [1, 2, 3],
            "col_3": [11, 22, 33],
        },
    )

    @spy
    def calc():
        return [df1, df2]

    # when
    calc()
    # then
    files = get_all_genereated_files(path=path)
    pd.testing.assert_frame_equal(df1, pd.read_csv(files[0], index_col=0))
    pd.testing.assert_frame_equal(df2, pd.read_csv(files[1], index_col=0))


def test_spy_in_one_series_one_func(path: Path) -> None:
    # given
    value = pd.Series(data=[1, 2, 3], name="0")

    @spy
    def calc(value):
        pass

    # when
    calc(value=value)
    # then
    files = get_all_genereated_files(path=path)
    assert value.to_list() == json.loads(files[0].read_text())
    # pd.testing.assert_series_equal(value, pd.read_csv(files[0], index_col=0)["0"])
