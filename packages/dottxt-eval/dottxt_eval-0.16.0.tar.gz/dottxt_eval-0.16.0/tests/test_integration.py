"""Integration tests for complete doteval workflows."""

import tempfile
from pathlib import Path

from doteval import ForEach
from doteval.evaluators import exact_match
from doteval.models import Result
from doteval.sessions import SessionManager


def test_complete_evaluation_workflow():
    """Test the full user workflow end-to-end."""
    # Create temporary directory for test storage
    with tempfile.TemporaryDirectory() as temp_dir:
        storage_path = Path(temp_dir)

        # Simple test dataset
        test_data = [
            ("What is 2+2?", "4"),
            ("What is 3+3?", "6"),
            ("What is 5+5?", "10"),
        ]

        # Create ForEach instance with storage
        foreach = ForEach(storage=f"json://{storage_path}")

        # Define evaluation function
        @foreach("question,answer", test_data)
        def eval_math(question, answer):
            # Create prompt
            prompt = f"Question: {question}"
            # Simulate some processing
            result = "4" if "2+2" in question else "wrong"
            # Return Result with prompt and scores
            return Result(exact_match(result, answer), prompt=prompt)

        # Run the evaluation with the new API
        result = eval_math(
            evaluation_name="eval_math", experiment_name="test_experiment", samples=None
        )

        # Verify results
        assert len(result.results) == 3
        assert (
            result.summary["exact_match"]["accuracy"] == 1 / 3
        )  # Only first item matches

        # Create session manager to verify storage
        session_manager = SessionManager(
            storage=f"json://{storage_path}", experiment_name="test_experiment"
        )

        # Verify experiment was created and evaluation persisted
        experiments = session_manager.storage.list_experiments()
        assert "test_experiment" in experiments

        # Verify we can retrieve the evaluation results
        results = session_manager.storage.get_results("test_experiment", "eval_math")
        assert len(results) == 3


def test_session_persistence_across_runs():
    """Test that session state persists across multiple runs."""
    with tempfile.TemporaryDirectory() as temp_dir:
        storage_path = Path(temp_dir)

        test_data = [("Q1", "A1"), ("Q2", "A2")]

        # Create ForEach instance with storage
        foreach = ForEach(storage=f"json://{storage_path}")

        @foreach("question,answer", test_data)
        def eval_test(question, answer):
            prompt = f"Q: {question}"
            return Result(exact_match(answer, "A1"), prompt=prompt)

        # First run
        result1 = eval_test(
            evaluation_name="eval_test",
            experiment_name="persistence_test",
            samples=None,
        )
        assert len(result1.results) == 2  # Verify first run processed items

        # Second run with new session manager (simulates new process)
        session_manager2 = SessionManager(
            storage=f"json://{storage_path}", experiment_name="persistence_test"
        )

        # Should be able to retrieve the same evaluation results
        results = session_manager2.storage.get_results("persistence_test", "eval_test")
        assert len(results) == 2

        # Experiments should be the same
        experiments = session_manager2.storage.list_experiments()
        assert "persistence_test" in experiments
