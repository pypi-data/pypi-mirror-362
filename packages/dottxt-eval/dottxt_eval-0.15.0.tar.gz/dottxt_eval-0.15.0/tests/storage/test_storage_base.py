"""Abstract base test class for storage implementations."""

import time
from abc import ABC, abstractmethod

import pytest
from PIL import Image

from doteval.metrics import accuracy
from doteval.models import Evaluation, EvaluationStatus, Record, Result, Score
from doteval.storage.base import Storage


class StorageTestBase(ABC):
    """Abstract base class for storage backend tests.

    Subclasses must implement the storage fixture that provides
    the specific storage implementation to test.
    """

    @abstractmethod
    @pytest.fixture
    def storage(self) -> Storage:
        """Provide storage implementation to test."""
        pass

    def test_create_experiment(self, storage):
        """Test creating an experiment."""
        experiment_name = "test_experiment"
        storage.create_experiment(experiment_name)

        experiments = storage.list_experiments()
        assert experiment_name in experiments

    def test_create_experiment_idempotent(self, storage):
        """Test creating same experiment twice is idempotent."""
        experiment_name = "test_exp"
        storage.create_experiment(experiment_name)
        storage.create_experiment(experiment_name)  # Should not raise

        experiments = storage.list_experiments()
        assert experiments.count(experiment_name) == 1

    def test_delete_experiment(self, storage):
        """Test deleting an experiment."""
        experiment_name = "exp_to_delete"
        storage.create_experiment(experiment_name)

        # Verify it exists
        assert experiment_name in storage.list_experiments()

        # Delete it
        storage.delete_experiment(experiment_name)

        # Verify it's gone
        assert experiment_name not in storage.list_experiments()

    def test_delete_nonexistent_experiment(self, storage):
        """Test deleting non-existent experiment raises error."""
        with pytest.raises(ValueError, match="not found"):
            storage.delete_experiment("nonexistent")

    def test_rename_experiment(self, storage):
        """Test renaming an experiment."""
        old_name = "old_exp"
        new_name = "new_exp"

        storage.create_experiment(old_name)
        storage.rename_experiment(old_name, new_name)

        experiments = storage.list_experiments()
        assert old_name not in experiments
        assert new_name in experiments

    def test_rename_nonexistent_experiment(self, storage):
        """Test renaming non-existent experiment raises error."""
        with pytest.raises(ValueError, match="not found"):
            storage.rename_experiment("nonexistent", "new_name")

    def test_rename_to_existing_experiment(self, storage):
        """Test renaming to existing name raises error."""
        storage.create_experiment("exp1")
        storage.create_experiment("exp2")

        with pytest.raises(ValueError, match="already exists"):
            storage.rename_experiment("exp1", "exp2")

    def test_list_experiments_empty(self, storage):
        """Test listing experiments when none exist."""
        experiments = storage.list_experiments()
        assert experiments == []

    def test_list_experiments_multiple(self, storage):
        """Test listing multiple experiments."""
        exp_names = ["exp1", "exp2", "exp3"]
        for name in exp_names:
            storage.create_experiment(name)

        experiments = storage.list_experiments()
        assert len(experiments) == 3
        assert set(experiments) == set(exp_names)

    def test_create_evaluation(self, storage):
        """Test creating an evaluation."""
        experiment_name = "test_exp"
        storage.create_experiment(experiment_name)

        evaluation = Evaluation(
            evaluation_name="test_eval",
            status=EvaluationStatus.RUNNING,
            started_at=time.time(),
            metadata={"key": "value"},
        )
        storage.create_evaluation(experiment_name, evaluation)

        evaluations = storage.list_evaluations(experiment_name)
        assert "test_eval" in evaluations

    def test_list_evaluations_empty(self, storage):
        """Test listing evaluations when none exist."""
        storage.create_experiment("test_exp")
        evaluations = storage.list_evaluations("test_exp")
        assert evaluations == []

    def test_list_evaluations_nonexistent_experiment(self, storage):
        """Test listing evaluations for non-existent experiment."""
        evaluations = storage.list_evaluations("nonexistent")
        assert evaluations == []

    def test_load_evaluation(self, storage):
        """Test loading an evaluation."""
        experiment_name = "test_exp"
        storage.create_experiment(experiment_name)

        original_eval = Evaluation(
            evaluation_name="test_eval",
            status=EvaluationStatus.RUNNING,
            started_at=1234567890,
            metadata={"test": "data"},
        )
        storage.create_evaluation(experiment_name, original_eval)

        loaded_eval = storage.load_evaluation(experiment_name, "test_eval")
        assert loaded_eval is not None
        assert loaded_eval.evaluation_name == "test_eval"
        assert loaded_eval.status == EvaluationStatus.RUNNING
        assert loaded_eval.started_at == 1234567890
        assert loaded_eval.metadata == {"test": "data"}

    def test_load_nonexistent_evaluation(self, storage):
        """Test loading non-existent evaluation returns None."""
        storage.create_experiment("test_exp")
        loaded = storage.load_evaluation("test_exp", "nonexistent")
        assert loaded is None

    def test_update_evaluation_status(self, storage):
        """Test updating evaluation status."""
        experiment_name = "test_exp"
        storage.create_experiment(experiment_name)

        evaluation = Evaluation(
            evaluation_name="test_eval",
            status=EvaluationStatus.RUNNING,
            started_at=time.time(),
        )
        storage.create_evaluation(experiment_name, evaluation)

        # Update status
        storage.update_evaluation_status(
            experiment_name, "test_eval", EvaluationStatus.COMPLETED
        )

        # Verify update
        loaded = storage.load_evaluation(experiment_name, "test_eval")
        assert loaded.status == EvaluationStatus.COMPLETED
        assert loaded.completed_at is not None

    def test_update_nonexistent_evaluation_status(self, storage):
        """Test updating status of non-existent evaluation raises error."""
        storage.create_experiment("test_exp")

        with pytest.raises(ValueError, match="not found"):
            storage.update_evaluation_status(
                "test_exp", "nonexistent", EvaluationStatus.COMPLETED
            )

    def test_add_results(self, storage):
        """Test adding results to an evaluation."""
        experiment_name = "test_exp"
        storage.create_experiment(experiment_name)

        evaluation = Evaluation(
            evaluation_name="test_eval",
            status=EvaluationStatus.RUNNING,
            started_at=time.time(),
        )
        storage.create_evaluation(experiment_name, evaluation)

        # Create results
        metric = accuracy()
        result = Result(
            Score("evaluator1", True, [metric], {"key": "value"}),
            prompt="test prompt",
        )
        record = Record(
            result=result,
            item_id=0,
            dataset_row={"input": "test", "expected": "test"},
            error=None,
            timestamp=time.time(),
        )

        storage.add_results(experiment_name, "test_eval", [record])

        # Verify results were added
        results = storage.get_results(experiment_name, "test_eval")
        assert len(results) == 1
        assert results[0].item_id == 0
        assert results[0].result.prompt == "test prompt"

    def test_add_results_nonexistent_evaluation(self, storage):
        """Test adding results to non-existent evaluation raises error."""
        storage.create_experiment("test_exp")

        result = Result(prompt="test")
        record = Record(result=result, item_id=0, dataset_row={})

        with pytest.raises(ValueError):
            storage.add_results("test_exp", "nonexistent", [record])

    def test_get_results_empty(self, storage):
        """Test getting results when none exist."""
        experiment_name = "test_exp"
        storage.create_experiment(experiment_name)

        evaluation = Evaluation(
            evaluation_name="test_eval",
            status=EvaluationStatus.RUNNING,
            started_at=time.time(),
        )
        storage.create_evaluation(experiment_name, evaluation)

        results = storage.get_results(experiment_name, "test_eval")
        assert results == []

    def test_get_results_nonexistent_evaluation(self, storage):
        """Test getting results for non-existent evaluation."""
        storage.create_experiment("test_exp")
        results = storage.get_results("test_exp", "nonexistent")
        assert results == []

    def test_completed_items(self, storage):
        """Test getting completed item IDs."""
        experiment_name = "test_exp"
        storage.create_experiment(experiment_name)

        evaluation = Evaluation(
            evaluation_name="test_eval",
            status=EvaluationStatus.RUNNING,
            started_at=time.time(),
        )
        storage.create_evaluation(experiment_name, evaluation)

        # Add some results
        results = []
        for i in range(5):
            result = Result(prompt=f"test{i}")
            record = Record(result=result, item_id=i, dataset_row={})
            results.append(record)

        storage.add_results(experiment_name, "test_eval", results)

        # Get completed items
        completed = storage.completed_items(experiment_name, "test_eval")
        assert set(completed) == {0, 1, 2, 3, 4}

    def test_completed_items_empty(self, storage):
        """Test completed items when evaluation has no results."""
        experiment_name = "test_exp"
        storage.create_experiment(experiment_name)

        evaluation = Evaluation(
            evaluation_name="test_eval",
            status=EvaluationStatus.RUNNING,
            started_at=time.time(),
        )
        storage.create_evaluation(experiment_name, evaluation)

        completed = storage.completed_items(experiment_name, "test_eval")
        assert completed == []

    def test_completed_items_nonexistent_evaluation(self, storage):
        """Test completed items for non-existent evaluation."""
        storage.create_experiment("test_exp")
        completed = storage.completed_items("test_exp", "nonexistent")
        assert completed == []

    def test_results_with_errors(self, storage):
        """Test storing and retrieving results with errors."""
        experiment_name = "test_exp"
        storage.create_experiment(experiment_name)

        evaluation = Evaluation(
            evaluation_name="test_eval",
            status=EvaluationStatus.RUNNING,
            started_at=time.time(),
        )
        storage.create_evaluation(experiment_name, evaluation)

        # Create result with error
        result = Result(prompt="")
        record = Record(
            result=result,
            item_id=0,
            dataset_row={"input": "test"},
            error="ValueError: Test error",
            timestamp=time.time(),
        )

        storage.add_results(experiment_name, "test_eval", [record])

        # Verify error is preserved
        results = storage.get_results(experiment_name, "test_eval")
        assert len(results) == 1
        assert results[0].error == "ValueError: Test error"

    def test_results_with_images(self, storage):
        """Test storing and retrieving results with PIL images."""
        experiment_name = "test_exp"
        storage.create_experiment(experiment_name)

        evaluation = Evaluation(
            evaluation_name="test_eval",
            status=EvaluationStatus.RUNNING,
            started_at=time.time(),
        )
        storage.create_evaluation(experiment_name, evaluation)

        # Create result with image
        img = Image.new("RGB", (10, 10), color="red")
        result = Result(prompt="test")
        record = Record(
            result=result,
            item_id=0,
            dataset_row={"image": img, "text": "test"},
        )

        storage.add_results(experiment_name, "test_eval", [record])

        # Verify image is preserved
        results = storage.get_results(experiment_name, "test_eval")
        assert len(results) == 1
        assert isinstance(results[0].dataset_row["image"], Image.Image)
        assert results[0].dataset_row["image"].size == (10, 10)

    def test_multiple_evaluations_per_experiment(self, storage):
        """Test multiple evaluations in one experiment."""
        experiment_name = "test_exp"
        storage.create_experiment(experiment_name)

        # Create multiple evaluations
        for i in range(3):
            evaluation = Evaluation(
                evaluation_name=f"eval_{i}",
                status=EvaluationStatus.RUNNING,
                started_at=time.time(),
            )
            storage.create_evaluation(experiment_name, evaluation)

        evaluations = storage.list_evaluations(experiment_name)
        assert len(evaluations) == 3
        assert set(evaluations) == {"eval_0", "eval_1", "eval_2"}

    def test_experiment_isolation(self, storage):
        """Test that experiments are isolated from each other."""
        # Create two experiments with evaluations
        for exp_num in range(2):
            exp_name = f"exp_{exp_num}"
            storage.create_experiment(exp_name)

            evaluation = Evaluation(
                evaluation_name="same_eval_name",
                status=EvaluationStatus.RUNNING,
                started_at=time.time(),
            )
            storage.create_evaluation(exp_name, evaluation)

            # Add different results to each
            result = Result(prompt=f"prompt_{exp_num}")
            record = Record(result=result, item_id=exp_num, dataset_row={})
            storage.add_results(exp_name, "same_eval_name", [record])

        # Verify results are isolated
        results_0 = storage.get_results("exp_0", "same_eval_name")
        results_1 = storage.get_results("exp_1", "same_eval_name")

        assert len(results_0) == 1
        assert len(results_1) == 1
        assert results_0[0].item_id == 0
        assert results_1[0].item_id == 1
        assert results_0[0].result.prompt == "prompt_0"
        assert results_1[0].result.prompt == "prompt_1"
