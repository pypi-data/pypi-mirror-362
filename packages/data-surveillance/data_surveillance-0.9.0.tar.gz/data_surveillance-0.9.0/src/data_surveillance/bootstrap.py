import os
from pathlib import Path
from random import randint
import logging
from logging import StreamHandler

if _path := os.environ.get("_SPY_RESULTS_DIR"):
    SPY_RESULTS_DIR = Path(_path)
else:
    SPY_RESULTS_DIR = Path.cwd() / f".{randint(1000, 9999)}"


HASH_OUTPUT_FILE_NAME: str = ".hashed.json"


logger = logging.getLogger(__name__)
logger.addHandler(StreamHandler())
logger.setLevel(logging.INFO)
