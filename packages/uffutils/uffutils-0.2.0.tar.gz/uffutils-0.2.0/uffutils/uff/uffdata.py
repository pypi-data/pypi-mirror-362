from __future__ import annotations

from typing import Generator

from uffutils.uff.dataset import (
    Dataset,
    IScaleable,
    ISubsetable,
    UFF15Dataset,
    UFF55Dataset,
)


class UFFData:
    """
    Represents UFFData from a file. Couple of limitations / assumptions:
    - Assumes exactly one UFF15 dataset to be present
    - Currently only understands UFF15, 18 and 55

    It requires data in the structure specified by our friends from PyUFF,
    making it play nicely with that.
    """

    _datasets: list[Dataset]
    _uff15: UFF15Dataset

    def __init__(self, datasets: list[dict]):
        self._datasets = []
        for ds in datasets:
            if ds["type"] == 15:
                self._uff15 = UFF15Dataset(ds)
                self._datasets.append(self._uff15)
            elif ds["type"] == 55:
                self._datasets.append(UFF55Dataset(ds))
            else:
                self._datasets.append(Dataset(ds))

    def __len__(self):
        return self._datasets.__len__()

    def get_set_types(self) -> list[int]:
        return [ds.type for ds in self._datasets]

    def get_set_type_count(self) -> dict:
        d: dict = {}
        for t in self.get_set_types():
            if t in d:
                d[t] += 1
            else:
                d[t] = 1
        return d

    def get_nodes(self) -> list[int]:
        return self._uff15.node_nums

    def subset(
        self,
        target_nodes: list[int] | None = None,
        step: int | None = None,
        n_max: int | None = None,
    ):
        if not target_nodes:
            target_nodes = self.get_nodes()
        if step:
            target_nodes = target_nodes[::step]
        if n_max:
            target_nodes = target_nodes[:n_max]
        target_nodes_set = set(target_nodes)
        for ds in self._datasets:
            if isinstance(ds, ISubsetable):
                ds.subset(target_nodes_set)

    def scale(self, length: float = 1.0) -> None: 
        for ds in self._datasets: 
            if isinstance(ds, IScaleable):
                ds.scale(length=length)

    def rotate(self, r_x, r_y, r_z) -> None: ...

    def translate(self, x, y, z) -> None: ...

    def cs_to_global(self) -> None: ...

    def export(self) -> Generator[dict]:
        for ds in self._datasets:
            yield ds.export()

    def _validate(self) -> None:
        # Check UFF15 constraint
        if self.get_set_types().count(15) != 1:
            raise Exception("Should have exactly one UFF15 dataset.")
