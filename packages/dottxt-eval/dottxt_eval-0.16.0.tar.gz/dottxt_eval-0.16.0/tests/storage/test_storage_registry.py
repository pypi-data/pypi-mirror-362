"""Test the storage registry system for extensibility."""

import time
from typing import Optional

import pytest

from doteval.models import Evaluation, EvaluationStatus, Record
from doteval.storage.base import Storage


class MockStorage(Storage):
    """A mock storage backend for testing."""

    def __init__(self, path: str):
        self.path = path
        self.experiments: dict[str, dict] = {}  # experiment_name -> {evaluations: {}}

    def create_experiment(self, experiment_name: str):
        """Create an experiment. Idempotent."""
        if experiment_name not in self.experiments:
            self.experiments[experiment_name] = {"evaluations": {}}

    def delete_experiment(self, experiment_name: str):
        if experiment_name in self.experiments:
            del self.experiments[experiment_name]
        else:
            raise ValueError(f"Experiment '{experiment_name}' not found.")

    def rename_experiment(self, old_name: str, new_name: str):
        if old_name in self.experiments:
            self.experiments[new_name] = self.experiments.pop(old_name)
        else:
            raise ValueError(f"Experiment '{old_name}' not found.")

    def list_experiments(self) -> list[str]:
        return list(self.experiments.keys())

    def create_evaluation(self, experiment_name: str, evaluation: Evaluation):
        if experiment_name not in self.experiments:
            raise ValueError(f"Experiment '{experiment_name}' not found.")
        self.experiments[experiment_name]["evaluations"][evaluation.evaluation_name] = {
            "evaluation": evaluation,
            "results": [],
        }

    def load_evaluation(
        self, experiment_name: str, evaluation_name: str
    ) -> Optional[Evaluation]:
        if experiment_name not in self.experiments:
            return None
        evals = self.experiments[experiment_name]["evaluations"]
        if evaluation_name not in evals:
            return None
        return evals[evaluation_name]["evaluation"]

    def update_evaluation_status(
        self, experiment_name: str, evaluation_name: str, status: EvaluationStatus
    ):
        if experiment_name not in self.experiments:
            raise ValueError(f"Experiment '{experiment_name}' not found.")
        evals = self.experiments[experiment_name]["evaluations"]
        if evaluation_name not in evals:
            raise ValueError(f"Evaluation '{evaluation_name}' not found.")
        evals[evaluation_name]["evaluation"].status = status
        if status == EvaluationStatus.COMPLETED:
            evals[evaluation_name]["evaluation"].completed_at = time.time()

    def completed_items(self, experiment_name: str, evaluation_name: str) -> list[int]:
        if experiment_name not in self.experiments:
            return []
        evals = self.experiments[experiment_name]["evaluations"]
        if evaluation_name not in evals:
            return []
        results = evals[evaluation_name]["results"]
        return [r.item_id for r in results if r.error is None]

    def list_evaluations(self, experiment_name: str) -> list[str]:
        if experiment_name not in self.experiments:
            return []
        return list(self.experiments[experiment_name]["evaluations"].keys())

    def add_results(
        self,
        experiment_name: str,
        evaluation_name: str,
        results: list[Record],
    ):
        if experiment_name not in self.experiments:
            raise ValueError(f"Experiment '{experiment_name}' not found.")
        evals = self.experiments[experiment_name]["evaluations"]
        if evaluation_name not in evals:
            raise ValueError(f"Evaluation '{evaluation_name}' not found.")
        evals[evaluation_name]["results"].extend(results)

    def get_results(self, experiment_name: str, evaluation_name: str) -> list[Record]:
        if experiment_name not in self.experiments:
            return []
        evals = self.experiments[experiment_name]["evaluations"]
        if evaluation_name not in evals:
            return []
        return evals[evaluation_name]["results"]

    def remove_error_result(
        self, experiment_name: str, evaluation_name: str, item_id: int
    ):
        """Remove an errored result for a specific item that will be retried."""
        if experiment_name not in self.experiments:
            return
        evals = self.experiments[experiment_name]["evaluations"]
        if evaluation_name not in evals:
            return
        results = evals[evaluation_name]["results"]
        # Remove any error result for this item
        evals[evaluation_name]["results"] = [
            r for r in results if not (r.item_id == item_id and r.error is not None)
        ]

    def remove_error_results_batch(
        self, experiment_name: str, evaluation_name: str, item_ids: list[int]
    ):
        """Remove multiple errored results in batch."""
        if experiment_name not in self.experiments:
            return
        evals = self.experiments[experiment_name]["evaluations"]
        if evaluation_name not in evals:
            return
        item_ids_set = set(item_ids)
        results = evals[evaluation_name]["results"]
        # Remove any error results for these items
        evals[evaluation_name]["results"] = [
            r
            for r in results
            if not (r.item_id in item_ids_set and r.error is not None)
        ]


def test_register_custom_backend():
    """Test registering a custom storage backend."""
    from doteval.storage import get_storage, register

    # Register the mock backend
    register("mock", MockStorage)

    # Create storage using the custom backend
    storage = get_storage("mock://test/path")

    assert isinstance(storage, MockStorage)
    assert storage.path == "test/path"


def test_get_storage_with_unknown_backend():
    """Test that unknown backends raise an error."""
    from doteval.storage import get_storage

    with pytest.raises(ValueError, match="Unknown storage backend: unknown"):
        get_storage("unknown://path")


def test_backward_compatibility(tmp_path):
    """Test that existing storage paths still work."""
    from doteval.storage import get_storage
    from doteval.storage.json import JSONStorage

    # Test JSON backend
    json_path = tmp_path / "json_storage"
    json_storage = get_storage(f"json://{json_path}")
    assert isinstance(json_storage, JSONStorage)

    # SQLite backend is currently disabled
    # sqlite_path = tmp_path / "db.sqlite"
    # sqlite_storage = get_storage(f"sqlite://{sqlite_path}")
    # assert isinstance(sqlite_storage, SQLiteStorage)


def test_custom_backend_functionality():
    """Test that custom backends work with SessionManager."""
    from doteval.models import Result, Score
    from doteval.sessions import SessionManager
    from doteval.storage import register

    # Register mock backend
    register("mock", MockStorage)

    # Use it with SessionManager
    manager = SessionManager(storage="mock://memory", experiment_name="test_exp")

    # Start an evaluation
    manager.start_evaluation("test_eval")

    # Add some results
    result = Result(Score("evaluator", 1.0, [], {}), prompt="test")
    record = Record(result=result, item_id=0, dataset_row={})
    manager.add_results("test_eval", [record])

    # Verify results are stored
    results = manager.get_results("test_eval")
    assert len(results) == 1
    assert results[0].item_id == 0


def test_list_backends():
    """Test listing available backends."""
    from doteval.storage import list_backends, register

    # Register a test backend
    register("test_backend", MockStorage)

    backends = list_backends()
    assert "json" in backends
    # assert "sqlite" in backends  # Currently disabled
    assert "test_backend" in backends


def test_reregister_backend():
    """Test that re-registering a backend overwrites the previous one."""
    from doteval.storage import get_storage, register

    class AnotherMockStorage(MockStorage):
        pass

    # Register first version
    register("retest", MockStorage)
    storage1 = get_storage("retest://path")
    assert isinstance(storage1, MockStorage)

    # Re-register with different class
    register("retest", AnotherMockStorage)
    storage2 = get_storage("retest://path")
    assert isinstance(storage2, AnotherMockStorage)


def test_storage_path_without_protocol(tmp_path):
    """Test that paths without protocol default to json."""
    from doteval.storage import get_storage
    from doteval.storage.json import JSONStorage

    # Path without protocol should default to JSON
    storage_path = tmp_path / "storage"
    storage = get_storage(str(storage_path))
    assert isinstance(storage, JSONStorage)
