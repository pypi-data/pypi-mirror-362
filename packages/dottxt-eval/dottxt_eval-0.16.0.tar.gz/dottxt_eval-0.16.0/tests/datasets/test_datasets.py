"""Improved tests for datasets module - focused on behavior, not implementation."""

from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from doteval import foreach
from doteval.datasets import get_dataset_info, list_available
from doteval.datasets.base import Dataset, DatasetRegistry
from doteval.evaluators import exact_match
from doteval.models import Result


class SimpleDataset(Dataset):
    """Minimal test dataset."""

    name = "simple"
    splits = ["test"]
    columns = ["input", "output"]

    def __init__(self, split, **kwargs):
        self.num_rows = 1

    def __iter__(self):
        yield ("question", "answer")


def test_registry_basic_operations():
    """Test core registry functionality."""
    registry = DatasetRegistry()

    # Register and retrieve
    registry.register(SimpleDataset)
    assert registry.get_dataset_class("simple") == SimpleDataset
    assert "simple" in registry.list_datasets()


def test_registry_prevents_duplicates():
    """Test registry prevents duplicate registrations of different classes."""
    registry = DatasetRegistry()

    # Registering the same class twice should be idempotent (no error)
    registry.register(SimpleDataset)
    registry.register(SimpleDataset)  # Should not raise

    # But registering a different class with the same name should raise
    class AnotherSimpleDataset(Dataset):
        name = "simple"  # Same name as SimpleDataset
        splits = ["train"]
        columns = ["data"]

        def __init__(self, split: str, **kwargs):
            self.data: list[Any] = []

        def __iter__(self):
            return iter(self.data)

    with pytest.raises(ValueError, match="already registered with a different class"):
        registry.register(AnotherSimpleDataset)


def test_registry_missing_dataset_error():
    """Test helpful error for missing datasets."""
    registry = DatasetRegistry()

    with pytest.raises(ValueError, match="Dataset 'missing' not found"):
        registry.get_dataset_class("missing")


def test_datasets_module_functions():
    """Test module-level convenience functions."""
    # Should work without errors (uses global registry)
    datasets = list_available()
    assert isinstance(datasets, list)

    # GSM8K should be auto-registered
    assert "gsm8k" in datasets

    # Should be able to get info
    info = get_dataset_info("gsm8k")
    assert info["name"] == "gsm8k"
    assert "question" in info["columns"]


@pytest.mark.parametrize(
    "split,kwargs",
    [
        ("test", {}),
        ("train", {"limit": 10}),
    ],
)
def test_foreach_registry_syntax(split, kwargs):
    """Test foreach.dataset_name() creates working decorators."""
    # Should create decorator without error
    decorator = getattr(foreach, "gsm8k")(split, **kwargs)
    assert callable(decorator)

    # Should decorate functions properly
    @decorator
    def dummy_eval(question, answer):
        return True

    assert callable(dummy_eval)


def test_foreach_nonexistent_dataset():
    """Test foreach with nonexistent dataset."""
    with pytest.raises(ValueError, match="not found"):
        foreach.nonexistent("test")


@patch("datasets.load_dataset")
def test_gsm8k_loader_basic_functionality(mock_load_dataset):
    """Test GSM8K loader core functionality."""
    # Mock minimal response
    mock_dataset = MagicMock()
    mock_dataset.info.splits = {"test": MagicMock(num_examples=2)}
    mock_dataset.__iter__ = lambda self: iter(
        [
            {"question": "What is 2+2?", "answer": "2+2=4\n#### 4"},
            {"question": "What is 3+3?", "answer": "Invalid format"},
        ]
    )
    mock_load_dataset.return_value = mock_dataset

    from doteval.datasets.gsm8k import GSM8K

    dataset = GSM8K("test")

    # Should extract valid answers only
    results = list(dataset)
    assert len(results) == 1
    assert results[0] == ("What is 2+2?", "2+2=4", "4")


@pytest.mark.parametrize(
    "answer_text,expected_reasoning,expected_answer",
    [
        ("Simple answer.\n#### 42", "Simple answer.", "42"),
        ("Negative number.\n#### -15", "Negative number.", "-15"),
        ("With comma.\n#### 1,234", "With comma.", "1,234"),
        ("No answer marker.", None, None),
    ],
)
@patch("datasets.load_dataset")
def test_gsm8k_answer_extraction_patterns(
    mock_load_dataset, answer_text, expected_reasoning, expected_answer
):
    """Test GSM8K answer extraction handles various formats."""
    from doteval.datasets.gsm8k import GSM8K

    mock_dataset = MagicMock()
    mock_dataset.__iter__ = lambda self: iter(
        [{"question": "Test", "answer": answer_text}]
    )
    mock_dataset.info.splits = {"test": MagicMock(num_examples=1)}
    mock_load_dataset.return_value = mock_dataset

    dataset = GSM8K("test")
    results = list(dataset)
    if expected_answer is not None:
        assert len(results) == 1
        assert results[0][1] == expected_reasoning  # reasoning
        assert results[0][2] == expected_answer  # answer
    else:
        assert len(results) == 0


def test_integration_foreach_with_registered_dataset():
    """Test complete flow: register dataset -> use with foreach."""
    # This tests the actual user workflow
    decorator = foreach.gsm8k("test")

    @decorator
    def test_eval(question, answer):
        return {"score": 1.0}

    # Should be callable (actual execution would need real dataset)
    assert callable(test_eval)

    # Verify it's set up for pytest integration
    assert hasattr(test_eval, "__wrapped__")


def test_abstract_dataset_enforcement():
    """Test that Dataset enforces abstract methods."""
    with pytest.raises(TypeError):
        Dataset()  # Should fail - __init__ and __iter__ not implemented


def test_foreach_registry_without_split():
    """Test foreach.dataset_name() creates decorator when split is omitted."""

    class NoSplitDataset(Dataset):
        name = "no_split_dataset"
        splits = []
        columns = ["a", "b"]

        def __init__(self, **kwargs):
            self.num_rows = 1

        def __iter__(self):
            yield (10, 20)

    registry = DatasetRegistry()
    registry.register(NoSplitDataset)

    from doteval.core import foreach as core_foreach

    with patch("doteval.core._registry", registry):
        decorator = core_foreach.no_split_dataset()

        @decorator
        def eval_fn(a, b):
            return Result(exact_match(a, b), prompt="")

        # Should be callable (actual execution would need session context)
        assert callable(eval_fn)
        # Verify it's set up for pytest integration
        assert hasattr(eval_fn, "__wrapped__")
