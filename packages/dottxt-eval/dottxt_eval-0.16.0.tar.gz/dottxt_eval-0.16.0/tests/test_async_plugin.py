"""Test async evaluation execution in pytest plugin context."""

import asyncio
import json
import subprocess

from doteval.core import foreach
from doteval.evaluators import exact_match
from doteval.models import Result


def test_async_evaluation_executes_and_saves_results(tmp_path):
    """Test that async evaluation functions are properly executed and results are saved."""
    # Create a test file with an async evaluation
    test_file = tmp_path / "test_async_eval.py"
    test_file.write_text(
        f"""
import asyncio
from pathlib import Path
from doteval.core import ForEach
from doteval.evaluators import exact_match
from doteval.models import Result
from doteval.storage import JSONStorage

dataset = [("hello", "hello"), ("world", "world")]

# Create custom ForEach with storage configuration
custom_foreach = ForEach(storage=JSONStorage("{tmp_path}"))

@custom_foreach("input,expected", dataset)
async def test_async_evaluation(input, expected):
    # Add a small delay to ensure it's truly async
    await asyncio.sleep(0.001)

    # Create a marker file to prove this code executed
    marker = Path("async_eval_ran.txt")
    marker.write_text(f"Evaluated: {{input}}")

    return Result(
        exact_match(input, expected),
        prompt=f"Test: {{input}}"
    )
"""
    )

    # Run pytest on the test file with a session
    import subprocess

    result = subprocess.run(
        [
            "pytest",
            str(test_file),
            "-v",
            "--experiment",
            "test_async_experiment",
        ],
        capture_output=True,
        text=True,
        cwd=tmp_path,
    )

    # Check that the test passed
    assert result.returncode == 0, f"Test failed: {result.stdout}\n{result.stderr}"
    assert "1 passed" in result.stdout

    # Check that the async code actually ran
    marker_file = tmp_path / "async_eval_ran.txt"
    assert marker_file.exists(), "Async evaluation did not run"

    # Check that results were saved in JSONL format
    eval_file = (
        tmp_path / "test_async_experiment" / "test_async_evaluation[None-None].jsonl"
    )
    assert eval_file.exists(), "Evaluation file was not created"

    # Read JSONL file
    with open(eval_file) as f:
        lines = f.readlines()

    # First line is metadata
    metadata = json.loads(lines[0])
    assert metadata["evaluation_name"] == "test_async_evaluation[None-None]"
    assert metadata["status"] == "completed"

    # Remaining lines are results (filter out empty lines)
    results = [json.loads(line) for line in lines[1:] if line.strip()]
    assert len(results) == 2  # Two items in dataset

    # Verify the results content (order may vary due to async execution)
    inputs_found = [result["dataset_row"]["input"] for result in results]
    assert sorted(inputs_found) == ["hello", "world"]

    for result in results:
        assert (
            result["result"]["scores"][0]["value"] is True
        )  # exact_match should be True


def test_async_evaluation_with_concurrency(tmp_path):
    """Test async evaluation with concurrent execution."""
    test_file = tmp_path / "test_async_concurrent.py"
    test_file.write_text(
        f"""
import asyncio
from doteval.core import ForEach
from doteval.evaluators import exact_match
from doteval.models import Result
from doteval.storage import JSONStorage
from doteval.concurrency import SlidingWindowStrategy

# Larger dataset to test concurrency
dataset = [(f"item{{i}}", f"item{{i}}") for i in range(10)]

# Create custom ForEach with concurrency and storage configuration
custom_foreach = ForEach(
    concurrency=SlidingWindowStrategy(max_concurrency=5),
    storage=JSONStorage("{tmp_path}")
)

@custom_foreach("input,expected", dataset)
async def test_async_concurrent(input, expected):
    # Simulate some async work
    await asyncio.sleep(0.01)
    return Result(
        exact_match(input, expected),
        prompt=f"Test: {{input}}"
    )
"""
    )

    result = subprocess.run(
        [
            "pytest",
            str(test_file),
            "-v",
            "--experiment",
            "test_concurrent_experiment",
        ],
        capture_output=True,
        text=True,
        cwd=tmp_path,
    )

    assert result.returncode == 0, f"Test failed: {result.stdout}\n{result.stderr}"

    # Check results
    eval_file = (
        tmp_path
        / "test_concurrent_experiment"
        / "test_async_concurrent[None-None].jsonl"
    )
    with open(eval_file) as f:
        lines = f.readlines()

    # Skip metadata line and read results (filter out empty lines)
    results = [json.loads(line) for line in lines[1:] if line.strip()]
    assert len(results) == 10
    # Verify all succeeded
    for result in results:
        assert result["error"] is None
        assert result["result"]["scores"][0]["value"] is True


def test_async_and_sync_evaluations_together(tmp_path):
    """Test that async and sync evaluations can coexist."""
    test_file = tmp_path / "test_mixed_eval.py"
    test_file.write_text(
        f"""
import asyncio
from doteval.core import ForEach
from doteval.evaluators import exact_match
from doteval.models import Result
from doteval.storage import JSONStorage

dataset = [("test", "test")]

# Create custom ForEach with storage configuration
custom_foreach = ForEach(storage=JSONStorage("{tmp_path}"))

@custom_foreach("input,expected", dataset)
def test_sync_evaluation(input, expected):
    return Result(exact_match(input, expected), prompt=f"Sync: {{input}}")

@custom_foreach("input,expected", dataset)
async def test_async_evaluation(input, expected):
    await asyncio.sleep(0.001)
    return Result(exact_match(input, expected), prompt=f"Async: {{input}}")
"""
    )

    result = subprocess.run(
        [
            "pytest",
            str(test_file),
            "-v",
            "--experiment",
            "test_mixed_experiment",
        ],
        capture_output=True,
        text=True,
        cwd=tmp_path,
    )

    assert result.returncode == 0
    assert "2 passed" in result.stdout

    # Check both results are saved
    sync_file = (
        tmp_path / "test_mixed_experiment" / "test_sync_evaluation[None-None].jsonl"
    )
    async_file = (
        tmp_path / "test_mixed_experiment" / "test_async_evaluation[None-None].jsonl"
    )

    assert sync_file.exists(), "Sync evaluation file was not created"
    assert async_file.exists(), "Async evaluation file was not created"


def test_async_evaluation_error_handling(tmp_path):
    """Test that errors in async evaluations are properly handled."""
    test_file = tmp_path / "test_async_error.py"
    test_file.write_text(
        f"""
import asyncio
from doteval.core import ForEach
from doteval.models import Result
from doteval.storage import JSONStorage

dataset = [("good", "good"), ("bad", "bad")]

# Create custom ForEach with storage configuration
custom_foreach = ForEach(storage=JSONStorage("{tmp_path}"))

@custom_foreach("input,expected", dataset)
async def test_async_with_error(input, expected):
    await asyncio.sleep(0.001)
    if input == "bad":
        raise ValueError("Intentional error")
    return Result(prompt=f"Test: {{input}}")
"""
    )

    result = subprocess.run(
        [
            "pytest",
            str(test_file),
            "-v",
            "--experiment",
            "test_error_experiment",
        ],
        capture_output=True,
        text=True,
        cwd=tmp_path,
    )

    # Test should pass even with errors in evaluation
    assert result.returncode == 0

    # Check that error is recorded
    eval_file = (
        tmp_path / "test_error_experiment" / "test_async_with_error[None-None].jsonl"
    )
    with open(eval_file) as f:
        lines = f.readlines()

    # Skip metadata line and read results (filter out empty lines)
    results = [json.loads(line) for line in lines[1:] if line.strip()]
    assert len(results) == 2

    # Sort results by dataset_row to ensure consistent order
    results = sorted(results, key=lambda r: r["dataset_row"]["input"])

    # "bad" should have error
    assert results[0]["error"] is not None
    assert "Intentional error" in results[0]["error"]

    # "good" should succeed
    assert results[1]["error"] is None


def test_async_evaluation_with_asyncio_run_error():
    """Test that our solution handles the asyncio.run() error correctly."""
    # This test verifies that we're not getting the "asyncio.run() cannot be called
    # from a running event loop" error that was the original issue

    # Create a simple async evaluation
    dataset = [("test", "test")]

    @foreach("input,expected", dataset)
    async def async_eval(input, expected):
        await asyncio.sleep(0.001)
        return Result(exact_match(input, expected), prompt=f"Test: {input}")

    # The function should be properly wrapped
    assert hasattr(async_eval, "_column_names")
    assert asyncio.iscoroutinefunction(async_eval.__wrapped__)

    # Calling it should return a coroutine when called with required parameters
    coro = async_eval(
        evaluation_name="test_eval", experiment_name="test_experiment", samples=None
    )
    assert asyncio.iscoroutine(coro)

    # Clean up
    coro.close()
