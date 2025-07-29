from abc import ABC, abstractmethod
from typing import Iterator, List, Optional, Tuple, Type


class Dataset(ABC):
    name: str
    splits: list[str]
    columns: list[str]
    num_rows: Optional[int] = None

    @abstractmethod
    def __init__(self, split: str, **kwargs):
        """Load dataset and prepare metadata like num_rows"""
        pass

    @abstractmethod
    def __iter__(self) -> Iterator[Tuple]:
        """Return iterator over dataset items"""
        pass


class DatasetRegistry:
    """Central registry for all datasets"""

    def __init__(self):
        self._dataset_classes: dict[str, Type[Dataset]] = {}

    def register(self, dataset_class: Type[Dataset]):
        name = dataset_class.name
        if name in self._dataset_classes:
            # Allow re-registration of the same class (idempotent)
            if self._dataset_classes[name] is dataset_class:
                return
            raise ValueError(
                f"Tried to register {name}, but it was already registered with a different class."
            )
        self._dataset_classes[name] = dataset_class

    def get_dataset_class(self, name: str) -> Type[Dataset]:
        if name not in self._dataset_classes:
            raise ValueError(
                f"Dataset '{name}' not found. "
                f"Available datasets: {self.list_datasets()}"
            )
        return self._dataset_classes[name]

    def list_datasets(self) -> List[str]:
        return list(self._dataset_classes.keys())


_registry = DatasetRegistry()
