import json
import os

import numpy as np
import pyuff

from .uff.uffdata import UFFData


def read(path: str) -> UFFData:
    path = os.path.abspath(path)
    uff = pyuff.UFF(path)
    data = uff.read_sets()
    return UFFData(data)


def write(path: str, data: UFFData, overwrite: bool = True) -> str:
    path = os.path.abspath(path)
    uff = pyuff.UFF(path)
    if overwrite:
        mode = "overwrite"
    else:
        mode = "add"
    ds = list(data.export())
    uff.write_sets(ds, mode)
    return path


def deserialize(data: str) -> list[dict]:
    return json.loads(data)


def serialize(data: list[dict]):
    for d in data:
        for key, value in d.items():
            if isinstance(value, np.ndarray):
                d[key] = value.tolist()
    return json.dumps(data)
