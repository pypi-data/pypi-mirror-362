import json
import os
from pathlib import Path
from typing import Any
from data_surveillance.spy import spy
import pytest
import pandas as pd
import os
from .conftest import get_all_genereated_files


def test_spy_in_one_constrain(path: Path) -> None:
    # given
    value = pd.DataFrame(
        {
            "col_1": [1, 2, 3],
            "col_2": [11, 22, 33],
        },
    )
    # expected
    expected_value = pd.DataFrame(
        {
            "col_2": [11, 22, 33],
        },
    )

    @spy(
        constrains=[
            (pd.DataFrame, lambda x: x.drop(columns=["col_1"]), "in"),
        ]
    )
    def calc(value):
        pass

    # when
    calc(value=value.copy())

    # then
    files = get_all_genereated_files(path=path)
    pd.testing.assert_frame_equal(expected_value, pd.read_csv(files[0], index_col=0))


def test_spy_in_two_constrains(path: Path) -> None:
    # given
    value = pd.DataFrame(
        {
            "col_1": [1, 2, 3],
            "col_2": [11, 22, 33],
            "col_3": [11, 22, 33],
        },
    )
    # expected
    expected_value = pd.DataFrame(
        {
            "col_2": [11, 22, 33],
        },
    )

    @spy(
        constrains=[
            (pd.DataFrame, lambda x: x.drop(columns=["col_1"]), "in"),
            (pd.DataFrame, lambda x: x.drop(columns=["col_3"]), "in"),
        ]
    )
    def calc(value):
        pass

    # when
    calc(value=value.copy())

    # then
    files = get_all_genereated_files(path=path)
    pd.testing.assert_frame_equal(expected_value, pd.read_csv(files[0], index_col=0))


def test_spy_in_out_constrains(path: Path) -> None:
    # given
    value = pd.DataFrame(
        {
            "col_1": [1, 2, 3],
            "col_2": [11, 22, 33],
            "col_3": [11, 22, 33],
        },
    )
    # expected
    expected_value = pd.DataFrame(
        {
            "col_2": [22, 44, 66],
        },
    )

    def advance(v: pd.DataFrame) -> pd.DataFrame:
        v["col_2"] = [22, 44, 66]
        return v

    @spy(
        constrains=[
            (pd.DataFrame, lambda x: x.drop(columns=["col_1"]), "both"),
            (pd.DataFrame, lambda x: x.drop(columns=["col_3"]), "both"),
            (pd.DataFrame, advance, "out"),
        ]
    )
    def calc(value):
        return value

    # when
    calc(value=value.copy())

    # then
    files = get_all_genereated_files(path=path)

    pd.testing.assert_frame_equal(expected_value, pd.read_csv(files[1], index_col=0))


def test_spy_in_out_constrains_v2(path: Path) -> None:
    # given
    value = pd.DataFrame(
        {
            "col_1": [1, 2, 3],
            "col_2": [11, 22, 33],
            "col_3": [11, 22, 33],
        },
    )
    # expected
    expected_value = pd.DataFrame(
        {
            "col_1": [1, 2, 3],
            "col_2": [22, 44, 66],
            "col_3": [11, 22, 33],
        },
    )

    def advance(v: pd.DataFrame) -> pd.DataFrame:
        v = v.copy()
        v["col_2"] = [22, 44, 66]
        return v

    @spy(
        constrains=[
            (pd.DataFrame, lambda x: x.drop(columns=["col_1"]), "in"),
            (pd.DataFrame, lambda x: x.drop(columns=["col_3"]), "in"),
            (pd.DataFrame, advance, "out"),
        ]
    )
    def calc(value):
        return value

    # when
    calc(value=value.copy())

    # then
    files = get_all_genereated_files(path=path)

    pd.testing.assert_frame_equal(expected_value, pd.read_csv(files[1], index_col=0))
