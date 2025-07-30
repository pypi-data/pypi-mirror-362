from typing import Any, Iterable


class SubsetMap:
    def __init__(
        self,
        nodes: Iterable[int],
        target_nodes: Iterable[int],
        required_fields: list[str],
        optional_fields: list[str] | None = None,
    ):
        if not isinstance(target_nodes, set):
            target_nodes = set(target_nodes)
        else:
            target_nodes = target_nodes

        self._idx = [i for i, n in (enumerate(nodes)) if n in target_nodes]
        self._required_fields = required_fields
        if optional_fields:
            self._optional_fields = optional_fields
        else:
            self._optional_fields = []

    def apply(self, ds: dict[str, Any]) -> None:
        for k in self._required_fields:
            ds[k] = self._get_subset_by_idx(ds[k], self._idx)
        for k in self._optional_fields:
            try:
                ds[k] = self._get_subset_by_idx(ds[k], self._idx)
            except KeyError:
                # This is no biggie
                ...

    @staticmethod
    def _get_subset_by_idx(data: list, idx: list[int]) -> list:
        return [data[i] for i in idx]
