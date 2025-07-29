from __future__ import annotations

import abc


class Mergeable(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_start_index(self, *args: object) -> int:
        pass

    @abc.abstractmethod
    def can_merge(self, other: Mergeable, *args: object) -> bool:
        pass

    @abc.abstractmethod
    def merge(self, other: Mergeable, *args: object) -> Mergeable:
        pass
