import json
import os
from pathlib import Path
import pickle
from typing import Any, Callable, Iterable, Literal

import pandas as pd
import logging
from logging import StreamHandler
from .bootstrap import SPY_RESULTS_DIR

logger = logging.getLogger(__name__)
logger.addHandler(StreamHandler())
logger.setLevel(logging.INFO)


def _save(
    root_folder: Path,
    step: int,
    value: Any,
    key: None | str = None,
    opt_type: Literal["in", "out", ""] = "in",
    file_name: str = "",
) -> None:
    _step = f"0{step}" if step < 10 else str(step)

    file_name += f"{opt_type}__{_step}__type={type(value).__name__}"

    if key:
        file_name = f"{file_name}__key={key}"

    if isinstance(value, pd.Series):
        file_name += ".json"
        _value = sorted(value.to_list())
        with root_folder.joinpath(file_name).open("w") as f:
            f.writelines(json.dumps(_value))
    elif isinstance(value, pd.DataFrame):
        _value = value.copy()
        _value = _value.sort_index(axis=1)  # sor ccols
        _value = _value.sort_values(by=[_ for _ in _value.columns])
        _value = _value.reset_index(drop=True)

        file_name += ".csv"
        _value.to_csv(root_folder.joinpath(file_name))
    elif (
        isinstance(value, (list, tuple))
        and len(value) > 0
        and any(isinstance(_, (pd.DataFrame, pd.Series)) for _ in value)
    ):
        for i, element in enumerate(value):
            _save(root_folder, i, element, None, "", file_name)
    else:
        try:
            to_file = json.dumps(value)
            file_name += ".json"
        except TypeError as ex:
            logger.debug(ex.args[0])
            to_file = str(pickle.dumps(value))
            file_name += ".pickle"

        with root_folder.joinpath(file_name).open("w") as f:
            f.writelines(to_file)


def spy(func) -> Callable:
    path = SPY_RESULTS_DIR

    if not path.exists():
        path.mkdir(exist_ok=True)

    def inner(*arg, **kwargs):  # noqa: ANN002, ANN003, ANN202
        counter_file = path / ".counter"
        if counter_file.exists():
            step = counter_file.read_text()
            step = "0" if step == "" else str(int(step) + 1)
            counter_file.write_text(step)
        else:
            step = "0"
            counter_file.write_text(step)

        _step = f"0{step}" if int(step) < 10 else str(step)

        step_folder = path.joinpath(f"step_{_step}__{func.__qualname__}")
        step_folder.mkdir(exist_ok=True)

        small_step = 0
        for v in arg:
            _save(step_folder, small_step, v, None, "in")
            small_step += 1

        for k, v in kwargs.items():
            _save(step_folder, small_step, v, k, "in")
            small_step += 1

        r = func(*arg, **kwargs)
        if r is None:
            return None

        if isinstance(r, (list, tuple)):
            for _ in r:
                _save(step_folder, small_step, _, None, "out")
                small_step += 1
        else:
            _save(step_folder, small_step, r, None, "out")
        return r

    return inner


# # TODO: catch input output X
# # TODO: do numbers {00, 01} not {0,1} X
# # TODO: add other python objects X
# # TODO: Add hash comaprison X

# # TODO: add script which adding to every function my decorator:) -> orders with @staticfunction
