from collections import Counter

from uffutils.uff.dataset import Dataset
from uffutils.uff.uffdata import UFFData


class UFFDataViewer:
    def __init__(self, data: UFFData):
        self._nodes_viewer = NodesViewer(data.get_nodes())
        self._sets_viewer = SetsViewer(data._datasets)

    def print_summary(self) -> str:
        return (
            self._nodes_viewer.print_summary()
            + "\n"
            + self._sets_viewer.print_summary()
        )

    def print_nodes(self) -> str:
        return self._nodes_viewer.print_full()


class NodesViewer:
    def __init__(self, node_nums: list[int]):
        self._node_nums = node_nums

    def print_full(self) -> str:
        return ", ".join([str(i) for i in self._node_nums])

    def print_summary(self) -> str:
        s = "Nodes:\n"
        s += f"  Number of nodes: {len(self._node_nums)}\n"
        s += f"  Nodes: {nums_to_string(self._node_nums, truncate=True)}"
        return s


class SetsViewer:
    def __init__(self, sets: list[Dataset]):
        self._sets = sets

    def print_full(self):
        return nums_to_string(self._set_types(), truncate=False)

    def print_summary(self):
        s = "Sets:\n"
        s += f"  Set count: {len(self._sets)}\n"
        s += f"  Type count: {self._set_type_count_str()}\n"
        s += f"  Types: {nums_to_string(self._set_types(), truncate=True)}"
        return s

    def _set_types(self) -> list[int]:
        return [d.type for d in self._sets]

    def _set_type_count_str(self) -> str:
        c = []
        for k, v in self._set_type_count().items():
            c += [f"{k} ({v})"]
        return ", ".join(c)

    def _set_type_count(self) -> dict:
        return dict(Counter(self._set_types()))


def nums_to_string(nums: list[int], truncate=False) -> str:
    ns = [str(n) for n in nums]
    if truncate and len(ns) > 5:
        return ", ".join(ns[:2]) + ", ..., " + ", ".join(ns[-2:])
    else:
        return ", ".join(ns)
