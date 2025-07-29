"""Tests for SQLite storage implementation."""

import os
import sqlite3

import pytest

from doteval.metrics import accuracy
from doteval.models import Evaluation, EvaluationStatus, Record, Result, Score
from doteval.storage.sqlite import SQLiteStorage
from tests.storage.test_storage_base import StorageTestBase


class TestSQLiteStorage(StorageTestBase):
    """Test SQLite storage implementation."""

    @pytest.fixture
    def storage_path(self, tmp_path):
        """Create a temporary SQLite database path."""
        return str(tmp_path / "test.db")

    @pytest.fixture
    def storage(self, storage_path):
        """Create a SQLiteStorage instance."""
        return SQLiteStorage(storage_path)

    # SQLite-specific tests below

    def test_sqlite_storage_initialization(self, storage_path):
        """Test SQLiteStorage initialization creates database and tables."""
        _ = SQLiteStorage(storage_path)
        assert os.path.exists(storage_path)

        # Verify tables exist
        with sqlite3.connect(storage_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = {row[0] for row in cursor.fetchall()}
            expected_tables = {"experiments", "evaluations", "results", "scores"}
            assert expected_tables.issubset(tables)

    def test_foreign_key_constraints(self, storage):
        """Test that foreign key constraints are enforced."""
        # Create experiment and evaluation
        storage.create_experiment("test_exp")

        evaluation = Evaluation(
            evaluation_name="test_eval",
            status=EvaluationStatus.RUNNING,
            started_at=1234567890,
        )
        storage.create_evaluation("test_exp", evaluation)

        # Add a result
        result = Result(prompt="test")
        record = Record(result=result, item_id=0, dataset_row={})
        storage.add_results("test_exp", "test_eval", [record])

        # Delete experiment should cascade delete everything
        storage.delete_experiment("test_exp")

        # Verify everything is deleted
        assert "test_exp" not in storage.list_experiments()
        assert storage.list_evaluations("test_exp") == []
        assert storage.get_results("test_exp", "test_eval") == []

    def test_results_filtering_by_error(self, storage):
        """Test filtering results by error status."""
        storage.create_experiment("test_exp")

        evaluation = Evaluation(
            evaluation_name="test_eval",
            status=EvaluationStatus.RUNNING,
            started_at=1234567890,
        )
        storage.create_evaluation("test_exp", evaluation)

        # Add mixed results
        results = []
        for i in range(5):
            result = Result(prompt=f"test{i}")
            error = "Test error" if i % 2 == 0 else None
            record = Record(result=result, item_id=i, dataset_row={}, error=error)
            results.append(record)

        storage.add_results("test_exp", "test_eval", results)

        # Get all results and filter manually
        all_results = storage.get_results("test_exp", "test_eval")
        failed = [r for r in all_results if r.error is not None]
        assert len(failed) == 3  # Items 0, 2, 4
        assert all(r.error is not None for r in failed)
        assert [r.item_id for r in failed] == [0, 2, 4]

    def test_database_performance_with_large_dataset(self, storage):
        """Test performance with a large number of results."""
        storage.create_experiment("test_exp")

        evaluation = Evaluation(
            evaluation_name="test_eval",
            status=EvaluationStatus.RUNNING,
            started_at=1234567890,
        )
        storage.create_evaluation("test_exp", evaluation)

        # Add many results in batches
        batch_size = 100
        num_batches = 10

        for batch in range(num_batches):
            results = []
            for i in range(batch_size):
                item_id = batch * batch_size + i
                result = Result(prompt=f"test{item_id}")
                record = Record(
                    result=result, item_id=item_id, dataset_row={"index": item_id}
                )
                results.append(record)
            storage.add_results("test_exp", "test_eval", results)

        # Verify all results
        all_results = storage.get_results("test_exp", "test_eval")
        assert len(all_results) == batch_size * num_batches

        # Test completed items performance
        completed = storage.completed_items("test_exp", "test_eval")
        assert len(completed) == batch_size * num_batches

    def test_transaction_rollback_on_error(self, storage, storage_path):
        """Test that transactions are rolled back on error."""
        storage.create_experiment("test_exp")

        evaluation = Evaluation(
            evaluation_name="test_eval",
            status=EvaluationStatus.RUNNING,
            started_at=1234567890,
        )
        storage.create_evaluation("test_exp", evaluation)

        # Count initial results
        initial_results = len(storage.get_results("test_exp", "test_eval"))

        # Try to add results with an invalid reference
        # This should fail and rollback
        try:
            with sqlite3.connect(storage_path) as conn:
                conn.execute("PRAGMA foreign_keys = ON")
                cursor = conn.cursor()
                # Try to insert result with non-existent evaluation_id
                cursor.execute(
                    "INSERT INTO results (evaluation_id, item_id, dataset_row, error, timestamp) "
                    "VALUES (99999, 0, '{}', NULL, 0)"
                )
        except sqlite3.IntegrityError:
            pass  # Expected

        # Verify no partial data was committed
        final_results = len(storage.get_results("test_exp", "test_eval"))
        assert final_results == initial_results

    def test_sqlite_get_failed_results_with_filters(self, storage):
        """Test get_failed_results with evaluation and evaluator name filters."""
        storage.create_experiment("test_exp")

        # Create two evaluations
        eval1 = Evaluation(
            evaluation_name="eval1",
            status=EvaluationStatus.COMPLETED,
            started_at=1234567890,
        )
        eval2 = Evaluation(
            evaluation_name="eval2",
            status=EvaluationStatus.COMPLETED,
            started_at=1234567891,
        )
        storage.create_evaluation("test_exp", eval1)
        storage.create_evaluation("test_exp", eval2)

        # Add failed results to both evaluations
        acc_metric = accuracy()

        # Failed results for eval1
        result1 = Result(
            Score("evaluator1", False, [acc_metric], {}),
            Score("evaluator2", 0, [], {}),
            prompt="test1",
        )
        record1 = Record(result=result1, item_id=0, dataset_row={"input": "test1"})
        storage.add_results("test_exp", "eval1", [record1])

        # Failed results for eval2
        result2 = Result(
            Score("evaluator1", 0.0, [], {}),
            Score("evaluator3", False, [], {}),
            prompt="test2",
        )
        record2 = Record(result=result2, item_id=0, dataset_row={"input": "test2"})
        storage.add_results("test_exp", "eval2", [record2])

        # Test with evaluation filter
        failed = storage.get_failed_results("test_exp", evaluation_name="eval1")
        assert len(failed) == 2  # Two failed scores in eval1

        # Test with evaluator filter
        failed = storage.get_failed_results("test_exp", evaluator_name="evaluator1")
        assert len(failed) == 2  # evaluator1 failed in both evaluations

        # Test with both filters
        failed = storage.get_failed_results(
            "test_exp", evaluation_name="eval1", evaluator_name="evaluator2"
        )
        assert len(failed) == 1  # Only evaluator2 in eval1

    def test_sqlite_get_error_results_with_filter(self, storage):
        """Test get_error_results with evaluation name filter."""
        storage.create_experiment("test_exp")

        # Create two evaluations
        eval1 = Evaluation(
            evaluation_name="eval1",
            status=EvaluationStatus.COMPLETED,
            started_at=1234567890,
        )
        eval2 = Evaluation(
            evaluation_name="eval2",
            status=EvaluationStatus.COMPLETED,
            started_at=1234567891,
        )
        storage.create_evaluation("test_exp", eval1)
        storage.create_evaluation("test_exp", eval2)

        # Add results with errors
        # Error in eval1
        result1 = Result(prompt="")
        record1 = Record(
            result=result1,
            item_id=0,
            dataset_row={"input": "test1"},
            error="Error in eval1",
        )
        storage.add_results("test_exp", "eval1", [record1])

        # Error in eval2
        result2 = Result(prompt="")
        record2 = Record(
            result=result2,
            item_id=0,
            dataset_row={"input": "test2"},
            error="Error in eval2",
        )
        storage.add_results("test_exp", "eval2", [record2])

        # Test with evaluation filter
        errors = storage.get_error_results("test_exp", evaluation_name="eval1")
        assert len(errors) == 1
        assert errors[0]["error"] == "Error in eval1"

        # Test without filter
        errors = storage.get_error_results("test_exp")
        assert len(errors) == 2
