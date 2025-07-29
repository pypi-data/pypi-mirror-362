from typing import Optional, Type

from .base import Storage, _registry
from .json import JSONStorage
from .sqlite import SQLiteStorage

__all__ = [
    "Storage",
    "JSONStorage",
    "SQLiteStorage",
    "get_storage",
    "register",
    "list_backends",
]


def register(name: str, storage_class: Type[Storage]):
    """Register a storage backend.

    Args:
        name: The name of the backend (e.g., "json", "sqlite", "redis")
        storage_class: The storage class that implements the Storage interface
    """
    _registry.register(name, storage_class)


def list_backends() -> list[str]:
    """List all registered storage backend names."""
    return _registry.list_backends()


def get_storage(storage_path: Optional[str] = None) -> Storage:
    """Get a storage instance based on the storage path.

    The storage path format is: backend://path
    For backward compatibility, paths without a backend default to JSON.

    Args:
        storage_path: The storage path (e.g., "json://data", "sqlite://db.sqlite")

    Returns:
        A storage instance

    Raises:
        ValueError: If the backend is not registered
    """
    storage_path = "json://.doteval" if storage_path is None else storage_path

    if "://" in storage_path:
        backend_name, path = storage_path.split("://", 1)
    else:
        backend_name, path = "json", storage_path

    backend_class = _registry.get_backend(backend_name)

    return backend_class(path)  # type: ignore[call-arg]
