"""Concurrency strategies for doteval."""

from typing import Union

from .adaptive import AdaptiveStrategy
from .batch import BatchStrategy
from .sequential import SequentialStrategy
from .sliding_window import SlidingWindowStrategy

SyncConcurrencyStrategy = Union[BatchStrategy, SequentialStrategy]
AsyncConcurrencyStrategy = Union[SlidingWindowStrategy, AdaptiveStrategy]

__all__ = [
    "AdaptiveStrategy",
    "BatchStrategy",
    "SequentialStrategy",
    "SlidingWindowStrategy",
    "SyncConcurrencyStrategy",
    "AsyncConcurrencyStrategy",
]
