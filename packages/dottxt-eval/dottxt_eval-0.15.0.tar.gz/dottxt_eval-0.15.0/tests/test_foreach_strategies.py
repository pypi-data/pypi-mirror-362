"""Tests for ForEach decorator with custom strategies."""

import asyncio
from unittest.mock import patch

import pytest
from tenacity import AsyncRetrying, Retrying, stop_after_attempt, wait_fixed

from doteval import ForEach
from doteval.concurrency import BatchStrategy, SequentialStrategy, SlidingWindowStrategy
from doteval.models import Result
from doteval.storage import JSONStorage


class TestForEachWithStrategies:
    """Test ForEach decorator with custom retry and concurrency strategies."""

    def test_foreach_with_custom_retries(self):
        """Test ForEach with custom retry configuration."""
        custom_retries = AsyncRetrying(
            stop=stop_after_attempt(5),
            wait=wait_fixed(0.1),
        )

        foreach = ForEach(retries=custom_retries)

        # Test data
        dataset = [("input1",), ("input2",)]

        @foreach("text", dataset)
        def evaluate(text):
            return Result(1.0, prompt=text)

        # Mock the session manager
        with patch("doteval.core.SessionManager") as mock_sm:
            mock_sm.return_value.get_results.return_value = []

            # The function should use the custom retries
            assert foreach.retries == custom_retries

    def test_foreach_with_custom_concurrency_sync(self):
        """Test ForEach with custom concurrency for sync functions."""
        batch_strategy = BatchStrategy(batch_size=2)
        foreach = ForEach(concurrency=batch_strategy)

        dataset = [(f"input{i}",) for i in range(5)]

        @foreach("text", dataset)
        def evaluate(text):
            return Result(1.0, prompt=text)

        # The function should use the batch strategy
        assert foreach.concurrency == batch_strategy

    @pytest.mark.asyncio
    async def test_foreach_with_custom_concurrency_async(self):
        """Test ForEach with custom concurrency for async functions."""
        sliding_strategy = SlidingWindowStrategy(max_concurrency=3)
        foreach = ForEach(concurrency=sliding_strategy)

        dataset = [(f"input{i}",) for i in range(5)]

        @foreach("text", dataset)
        async def evaluate(text):
            await asyncio.sleep(0.001)
            return Result(1.0, prompt=text)

        # The function should use the sliding window strategy
        assert foreach.concurrency == sliding_strategy

    def test_foreach_with_custom_storage(self):
        """Test ForEach with custom storage backend."""
        # Use a temporary directory for testing
        import tempfile

        with tempfile.TemporaryDirectory() as tmpdir:
            custom_storage = JSONStorage(tmpdir)
            foreach = ForEach(storage=custom_storage)

            dataset = [("input1",), ("input2",)]

            @foreach("text", dataset)
            def evaluate(text):
                return Result(1.0, prompt=text)

            # The function should use the custom storage
            assert foreach.storage == custom_storage

    def test_foreach_initialization_with_name(self):
        """Test ForEach initialization without name (name parameter removed)."""
        foreach = ForEach()
        dataset = [("input1",), ("input2",)]

        # Dataset is provided in decorator call
        @foreach("text", dataset)
        def evaluate(text):
            return Result(1.0, prompt=text)

        # Name is no longer a parameter of ForEach
        assert hasattr(evaluate, "_column_names")

    def test_foreach_with_dataset(self):
        """Test that decorator properly uses the provided dataset."""
        decorator_dataset = [("dec1",), ("dec2",)]

        foreach = ForEach()

        @foreach("text", decorator_dataset)
        def evaluate(text):
            return Result(1.0, prompt=text)

        # The function should have column spec
        assert hasattr(evaluate, "_column_names")
        assert evaluate._column_names == ["text"]

    def test_foreach_missing_dataset_error(self):
        """Test error when no dataset is provided."""
        foreach = ForEach()

        with pytest.raises(
            TypeError, match="missing 1 required positional argument: 'dataset'"
        ):

            @foreach("text")
            def evaluate(text):
                return Result(1.0, prompt=text)

    def test_foreach_incompatible_strategy_error_sync(self):
        """Test error when async strategy is used with sync function."""
        sliding_strategy = SlidingWindowStrategy()
        foreach = ForEach(concurrency=sliding_strategy)

        dataset = [("input1",)]

        @foreach("text", dataset)
        def evaluate(text):
            return Result(1.0, prompt=text)

        # Attempting to run should raise an error when trying to iterate over async generator
        with pytest.raises(TypeError, match="'async_generator' object is not iterable"):
            evaluate(
                evaluation_name="test_eval",
                experiment_name="test_exp",
                samples=None,
            )

    @pytest.mark.asyncio
    async def test_foreach_incompatible_strategy_error_async(self):
        """Test error when sync strategy is used with async function."""

        sequential_strategy = SequentialStrategy()
        foreach = ForEach(concurrency=sequential_strategy)

        dataset = [("input1",)]

        @foreach("text", dataset)
        async def evaluate(text):
            return Result(1.0, prompt=text)

        # Attempting to run should raise an error when trying to async iterate over sync generator
        with pytest.raises(
            TypeError,
            match="'async for' requires an object with __aiter__ method, got generator",
        ):
            await evaluate(
                evaluation_name="test_eval",
                experiment_name="test_exp",
                samples=None,
            )

    def test_foreach_with_all_parameters(self):
        """Test ForEach with all parameters specified."""
        dataset = [("input1",), ("input2",)]
        custom_retries = Retrying(stop=stop_after_attempt(10))
        custom_concurrency = BatchStrategy(batch_size=5)
        custom_storage = JSONStorage("test_storage")

        foreach = ForEach(
            retries=custom_retries,
            concurrency=custom_concurrency,
            storage=custom_storage,
        )

        @foreach("text", dataset)
        def evaluate(text):
            return Result(1.0, prompt=text)

        assert foreach.retries == custom_retries
        assert foreach.concurrency == custom_concurrency
        assert foreach.storage == custom_storage
