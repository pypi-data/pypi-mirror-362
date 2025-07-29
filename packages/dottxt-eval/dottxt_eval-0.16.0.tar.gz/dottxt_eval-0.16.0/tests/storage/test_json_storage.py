"""Tests for JSON storage implementation."""

import json
import tempfile
from pathlib import Path

import pytest

from doteval.models import Evaluation, EvaluationStatus, Record, Result
from doteval.storage.json import JSONStorage
from tests.storage.test_storage_base import StorageTestBase


class TestJSONStorage(StorageTestBase):
    """Test JSON storage implementation."""

    @pytest.fixture
    def storage_dir(self, tmp_path):
        """Create a temporary directory for storage tests."""
        return tmp_path

    @pytest.fixture
    def storage(self, storage_dir):
        """Create a JSONStorage instance."""
        return JSONStorage(str(storage_dir))

    # JSON-specific tests below

    def test_json_storage_initialization(self, storage_dir):
        """Test JSONStorage initialization creates directory."""
        storage = JSONStorage(str(storage_dir))
        assert storage_dir.exists()
        assert storage.root_dir == storage_dir

    def test_json_file_structure(self, storage, storage_dir):
        """Test the JSON file structure created by storage."""
        experiment_name = "test_exp"
        storage.create_experiment(experiment_name)

        # Check experiment directory exists
        exp_dir = storage_dir / experiment_name
        assert exp_dir.exists()
        assert exp_dir.is_dir()

        # Create evaluation
        evaluation = Evaluation(
            evaluation_name="test_eval",
            status=EvaluationStatus.RUNNING,
            started_at=1234567890,
        )
        storage.create_evaluation(experiment_name, evaluation)

        # Check evaluation file exists
        eval_file = exp_dir / "test_eval.jsonl"
        assert eval_file.exists()

        # Check file content
        with open(eval_file) as f:
            first_line = json.loads(f.readline())
            assert first_line["evaluation_name"] == "test_eval"
            assert first_line["status"] == "running"
            assert first_line["started_at"] == 1234567890

    def test_jsonl_format(self, storage, storage_dir):
        """Test that results are stored in JSONL format."""
        experiment_name = "test_exp"
        storage.create_experiment(experiment_name)

        evaluation = Evaluation(
            evaluation_name="test_eval",
            status=EvaluationStatus.RUNNING,
            started_at=1234567890,
        )
        storage.create_evaluation(experiment_name, evaluation)

        # Add multiple results
        results = []
        for i in range(3):
            result = Result(prompt=f"test{i}")
            record = Record(result=result, item_id=i, dataset_row={"index": i})
            results.append(record)

        storage.add_results(experiment_name, "test_eval", results)

        # Check file format
        eval_file = storage_dir / experiment_name / "test_eval.jsonl"
        with open(eval_file) as f:
            lines = f.readlines()

        # First line is evaluation metadata
        assert len(lines) == 4  # 1 metadata + 3 results

        # Each line should be valid JSON
        for line in lines:
            json.loads(line)  # Should not raise

    def test_concurrent_writes(self, storage):
        """Test that concurrent writes append correctly."""
        experiment_name = "test_exp"
        storage.create_experiment(experiment_name)

        evaluation = Evaluation(
            evaluation_name="test_eval",
            status=EvaluationStatus.RUNNING,
            started_at=1234567890,
        )
        storage.create_evaluation(experiment_name, evaluation)

        # Add results in multiple batches
        for batch in range(3):
            results = []
            for i in range(2):
                item_id = batch * 2 + i
                result = Result(prompt=f"test{item_id}")
                record = Record(result=result, item_id=item_id, dataset_row={})
                results.append(record)
            storage.add_results(experiment_name, "test_eval", results)

        # Verify all results are present
        all_results = storage.get_results(experiment_name, "test_eval")
        assert len(all_results) == 6
        assert [r.item_id for r in all_results] == list(range(6))

    def test_corrupted_file_handling(self, storage, storage_dir):
        """Test handling of corrupted JSONL files."""
        experiment_name = "test_exp"
        storage.create_experiment(experiment_name)

        evaluation = Evaluation(
            evaluation_name="test_eval",
            status=EvaluationStatus.RUNNING,
            started_at=1234567890,
        )
        storage.create_evaluation(experiment_name, evaluation)

        # Add valid result
        result = Result(prompt="test")
        record = Record(result=result, item_id=0, dataset_row={})
        storage.add_results(experiment_name, "test_eval", [record])

        # Corrupt the file
        eval_file = storage_dir / experiment_name / "test_eval.jsonl"
        with open(eval_file, "a") as f:
            f.write("\n{ corrupted json }\n")

        # Should return empty list on corruption
        results = storage.get_results(experiment_name, "test_eval")
        assert results == []


# Additional JSON storage edge case tests from coverage file


def test_json_storage_create_existing_experiment():
    """Test creating an experiment that already exists (idempotent)."""
    with tempfile.TemporaryDirectory() as temp_dir:
        storage = JSONStorage(temp_dir)

        # Create experiment
        storage.create_experiment("test_exp")

        # Create same experiment again - should be idempotent
        storage.create_experiment("test_exp")

        # Should still have only one experiment
        experiments = storage.list_experiments()
        assert experiments.count("test_exp") == 1


def test_json_storage_delete_nonexistent_experiment():
    """Test deleting an experiment that doesn't exist."""
    with tempfile.TemporaryDirectory() as temp_dir:
        storage = JSONStorage(temp_dir)

        with pytest.raises(ValueError, match="Experiment 'nonexistent' not found"):
            storage.delete_experiment("nonexistent")


def test_json_storage_rename_nonexistent_experiment():
    """Test renaming an experiment that doesn't exist."""
    with tempfile.TemporaryDirectory() as temp_dir:
        storage = JSONStorage(temp_dir)

        with pytest.raises(ValueError, match="Experiment 'old_name' not found"):
            storage.rename_experiment("old_name", "new_name")


def test_json_storage_rename_to_existing_experiment():
    """Test renaming to an experiment name that already exists."""
    with tempfile.TemporaryDirectory() as temp_dir:
        storage = JSONStorage(temp_dir)

        # Create two experiments
        storage.create_experiment("exp1")
        storage.create_experiment("exp2")

        with pytest.raises(ValueError, match="Experiment 'exp2' already exists"):
            storage.rename_experiment("exp1", "exp2")


def test_json_storage_load_evaluation_with_corrupted_file():
    """Test loading evaluation when JSONL file is corrupted."""
    with tempfile.TemporaryDirectory() as temp_dir:
        storage = JSONStorage(temp_dir)
        storage.create_experiment("test_exp")

        # Create evaluation
        evaluation = Evaluation(
            evaluation_name="test_eval",
            status=EvaluationStatus.RUNNING,
            started_at=1234567890,
        )
        storage.create_evaluation("test_exp", evaluation)

        # Corrupt the file
        eval_file = Path(temp_dir) / "test_exp" / "test_eval.jsonl"
        with open(eval_file, "w") as f:
            f.write("{ invalid json }")

        # Loading corrupted file should either return None or raise JSONDecodeError
        try:
            loaded = storage.load_evaluation("test_exp", "test_eval")
            assert loaded is None
        except json.JSONDecodeError:
            # This is also acceptable behavior
            pass


def test_json_storage_update_nonexistent_evaluation():
    """Test updating status of non-existent evaluation."""
    with tempfile.TemporaryDirectory() as temp_dir:
        storage = JSONStorage(temp_dir)
        storage.create_experiment("test_exp")

        with pytest.raises(ValueError, match="Evaluation 'nonexistent' not found"):
            storage.update_evaluation_status(
                "test_exp", "nonexistent", EvaluationStatus.COMPLETED
            )


def test_json_storage_completed_items_nonexistent_file():
    """Test getting completed items when evaluation file doesn't exist."""
    with tempfile.TemporaryDirectory() as temp_dir:
        storage = JSONStorage(temp_dir)
        storage.create_experiment("test_exp")

        # Should return empty list
        items = storage.completed_items("test_exp", "nonexistent_eval")
        assert items == []


def test_json_storage_get_results_with_corrupted_line():
    """Test getting results when JSONL has a corrupted line."""
    with tempfile.TemporaryDirectory() as temp_dir:
        storage = JSONStorage(temp_dir)
        storage.create_experiment("test_exp")

        # Create evaluation
        evaluation = Evaluation(
            evaluation_name="test_eval",
            status=EvaluationStatus.RUNNING,
            started_at=1234567890,
        )
        storage.create_evaluation("test_exp", evaluation)

        # Add one valid result
        result = Result(prompt="test")
        record = Record(result=result, item_id=0, dataset_row={})
        storage.add_results("test_exp", "test_eval", [record])

        # Manually append a corrupted line
        eval_file = Path(temp_dir) / "test_exp" / "test_eval.jsonl"
        with open(eval_file, "a") as f:
            f.write("\n{ corrupted json line }\n")

        # The current implementation returns an empty list when encountering JSON errors
        results = storage.get_results("test_exp", "test_eval")
        assert results == []  # Returns empty list on JSON decode error


def test_json_storage_list_evaluations_no_experiment_dir():
    """Test listing evaluations when experiment directory doesn't exist."""
    with tempfile.TemporaryDirectory() as temp_dir:
        storage = JSONStorage(temp_dir)

        # Don't create the experiment
        evaluations = storage.list_evaluations("nonexistent_exp")
        assert evaluations == []
