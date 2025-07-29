"""Dataset management and discovery for doteval."""

from doteval.datasets.base import _registry

from . import bfcl, gsm8k, sroie  # noqa: F401
from .bfcl import BFCL as BFCL
from .gsm8k import GSM8K as GSM8K
from .sroie import SROIE as SROIE

__all__ = ["list_available", "get_dataset_info", "GSM8K", "SROIE"]


def list_available() -> list[str]:
    """List all available datasets that can be used with foreach.dataset_name()"""
    return _registry.list_datasets()


def get_dataset_info(name: str) -> dict:
    """Get information about a specific dataset"""
    dataset_class = _registry.get_dataset_class(name)
    return {
        "name": dataset_class.name,
        "splits": dataset_class.splits,
        "columns": dataset_class.columns,
        "num_rows": getattr(dataset_class, "num_rows", None),
    }
