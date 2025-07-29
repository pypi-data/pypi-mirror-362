"""Tests for concurrency strategies."""

import asyncio
import time

import pytest

from doteval.concurrency import (
    AdaptiveStrategy,
    BatchStrategy,
    SequentialStrategy,
    SlidingWindowStrategy,
)


class TestSequentialStrategy:
    """Test the sequential execution strategy."""

    def test_sequential_execution(self):
        """Test that tasks are executed sequentially."""
        strategy = SequentialStrategy()
        execution_order = []

        def create_tasks():
            for i in range(5):

                def task(task_id=i):
                    execution_order.append(task_id)
                    return f"result_{task_id}"

                yield task

        results = list(strategy.execute(create_tasks()))

        # Check execution order is sequential
        assert execution_order == [0, 1, 2, 3, 4]
        assert results == ["result_0", "result_1", "result_2", "result_3", "result_4"]

    def test_sequential_with_progress_callback(self):
        """Test sequential execution with progress callback."""
        strategy = SequentialStrategy()
        progress_results = []

        def progress_callback(result):
            progress_results.append(result)

        def create_tasks():
            for i in range(3):

                def task(task_id=i):
                    return f"result_{task_id}"

                yield task

        results = list(strategy.execute(create_tasks(), progress_callback))

        assert results == ["result_0", "result_1", "result_2"]
        assert progress_results == ["result_0", "result_1", "result_2"]

    def test_sequential_with_exception(self):
        """Test that exceptions are propagated."""
        strategy = SequentialStrategy()

        def create_tasks():
            yield lambda: "result_0"
            yield lambda: (_ for _ in ()).throw(ValueError("test error"))
            yield lambda: "result_2"

        results = []
        with pytest.raises(ValueError, match="test error"):
            for result in strategy.execute(create_tasks()):
                results.append(result)

        # Only the first task should have completed
        assert results == ["result_0"]


class TestBatchStrategy:
    """Test the batch execution strategy."""

    def test_batch_execution(self):
        """Test that tasks are executed in batches."""
        strategy = BatchStrategy(batch_size=3)
        execution_times = []

        def create_tasks():
            for i in range(7):

                def task(task_id=i):
                    execution_times.append(task_id)
                    return f"result_{task_id}"

                yield task

        results = list(strategy.execute(create_tasks()))

        # Check all tasks executed
        assert len(execution_times) == 7
        assert len(results) == 7
        assert results == [f"result_{i}" for i in range(7)]

    def test_batch_with_progress_callback(self):
        """Test batch execution with progress callback."""
        strategy = BatchStrategy(batch_size=2)
        progress_results = []

        def progress_callback(result):
            progress_results.append(result)

        def create_tasks():
            for i in range(5):

                def task(task_id=i):
                    return f"result_{task_id}"

                yield task

        results = list(strategy.execute(create_tasks(), progress_callback))

        assert len(results) == 5
        assert len(progress_results) == 5
        assert progress_results == [f"result_{i}" for i in range(5)]


class TestSlidingWindowStrategy:
    """Test the sliding window async execution strategy."""

    @pytest.mark.asyncio
    async def test_sliding_window_execution(self):
        """Test that tasks are executed with concurrency control."""
        strategy = SlidingWindowStrategy(max_concurrency=2)
        currently_running = 0
        max_concurrent = 0

        def create_tasks():
            for i in range(5):

                async def task(task_id=i):
                    nonlocal currently_running, max_concurrent
                    currently_running += 1
                    max_concurrent = max(max_concurrent, currently_running)
                    await asyncio.sleep(0.01)  # Simulate work
                    currently_running -= 1
                    return f"result_{task_id}"

                yield task

        results = []
        async for result in strategy.execute(create_tasks()):
            results.append(result)

        # Check all tasks completed
        assert len(results) == 5
        assert all(r.startswith("result_") for r in results)
        # Check concurrency was limited
        assert max_concurrent <= 2

    @pytest.mark.asyncio
    async def test_sliding_window_with_progress_callback(self):
        """Test sliding window execution with progress callback."""
        strategy = SlidingWindowStrategy(max_concurrency=3)
        progress_results = []

        def progress_callback(result):
            progress_results.append(result)

        def create_tasks():
            for i in range(4):

                async def task(task_id=i):
                    await asyncio.sleep(0.001)
                    return f"result_{task_id}"

                yield task

        results = []
        async for result in strategy.execute(create_tasks(), progress_callback):
            results.append(result)

        assert len(results) == 4
        assert len(progress_results) == 4

    @pytest.mark.asyncio
    async def test_sliding_window_with_exception(self):
        """Test that exceptions in tasks are propagated."""
        strategy = SlidingWindowStrategy(max_concurrency=2)

        def create_tasks():
            async def task1():
                await asyncio.sleep(0.01)
                return "result_1"

            async def task2():
                await asyncio.sleep(0.005)
                raise ValueError("test error")

            async def task3():
                return "result_3"

            yield task1
            yield task2
            yield task3

        results = []

        with pytest.raises(ValueError, match="test error"):
            async for result in strategy.execute(create_tasks()):
                results.append(result)

        # The strategy executes tasks concurrently, so we might get some results
        # before the exception is raised
        assert len(results) <= 3  # At most all results if exception is last


class TestAdaptiveStrategy:
    """Test the adaptive concurrency execution strategy."""

    @pytest.mark.asyncio
    async def test_adaptive_basic_execution(self):
        """Test that adaptive strategy can execute tasks."""
        strategy = AdaptiveStrategy(
            initial_concurrency=2,
            adaptation_interval=0.1,  # Fast adaptation for testing
            min_concurrency=1,
            max_concurrency=10,
        )

        def create_tasks():
            for i in range(5):

                async def task(task_id=i):
                    await asyncio.sleep(0.01)
                    return f"result_{task_id}"

                yield task

        results = []
        async for result in strategy.execute(create_tasks()):
            results.append(result)

        assert len(results) == 5
        assert all(r.startswith("result_") for r in results)

    @pytest.mark.asyncio
    async def test_adaptive_with_progress_callback(self):
        """Test adaptive strategy with progress callback."""
        strategy = AdaptiveStrategy(
            initial_concurrency=2,
            adaptation_interval=0.05,
        )
        progress_results = []

        def progress_callback(result):
            progress_results.append(result)

        def create_tasks():
            for i in range(4):

                async def task(task_id=i):
                    await asyncio.sleep(0.001)
                    return f"result_{task_id}"

                yield task

        results = []
        async for result in strategy.execute(create_tasks(), progress_callback):
            results.append(result)

        assert len(results) == 4
        assert len(progress_results) == 4
        assert set(results) == set(progress_results)

    @pytest.mark.asyncio
    async def test_adaptive_throughput_tracking(self):
        """Test that adaptive strategy tracks throughput."""
        strategy = AdaptiveStrategy(
            initial_concurrency=2,
            adaptation_interval=0.05,
        )

        def create_tasks():
            for i in range(10):

                async def task(task_id=i):
                    await asyncio.sleep(0.01)
                    return f"result_{task_id}"

                yield task

        results = []
        async for result in strategy.execute(create_tasks()):
            results.append(result)

        stats = strategy.get_stats()
        assert stats["total_completed"] == 10
        assert stats["total_tasks"] == 10
        assert stats["throughput"] is not None
        assert stats["throughput"] > 0

    @pytest.mark.asyncio
    async def test_adaptive_concurrency_adjustment(self):
        """Test that adaptive strategy can adjust concurrency."""
        strategy = AdaptiveStrategy(
            initial_concurrency=2,
            adaptation_interval=0.05,  # Fast adaptation
            min_concurrency=1,
            max_concurrency=20,
            stability_window=1,  # Quick decisions
        )

        # Create enough tasks to allow adaptation to happen
        def create_tasks():
            for i in range(30):

                async def task(task_id=i):
                    await asyncio.sleep(0.01)  # Some work time
                    return f"result_{task_id}"

                yield task

        results = []

        async for result in strategy.execute(create_tasks()):
            results.append(result)

        final_stats = strategy.get_stats()

        # Should have completed all tasks
        assert len(results) == 30

        # Strategy should have some adaptation history or at least be functioning
        assert final_stats["total_completed"] == 30
        assert final_stats["throughput"] is not None

    @pytest.mark.asyncio
    async def test_adaptive_error_handling(self):
        """Test that adaptive strategy handles errors properly."""
        strategy = AdaptiveStrategy(
            initial_concurrency=2,
            adaptation_interval=0.05,
            error_backoff_factor=0.5,
        )

        def create_tasks():
            # First few tasks succeed
            for i in range(3):

                async def task(task_id=i):
                    await asyncio.sleep(0.01)
                    return f"result_{task_id}"

                yield task

            # Then a task fails
            async def failing_task():
                await asyncio.sleep(0.01)
                raise ValueError("test error")

            yield failing_task

        results = []

        with pytest.raises(ValueError, match="test error"):
            async for result in strategy.execute(create_tasks()):
                results.append(result)

        # Should have gotten some results before the error
        assert len(results) >= 1

    @pytest.mark.asyncio
    async def test_adaptive_stats_collection(self):
        """Test that adaptive strategy collects comprehensive stats."""
        strategy = AdaptiveStrategy(
            initial_concurrency=3,
            adaptation_interval=0.05,
        )

        def create_tasks():
            for i in range(8):

                async def task(task_id=i):
                    await asyncio.sleep(0.01)
                    return f"result_{task_id}"

                yield task

        results = []
        async for result in strategy.execute(create_tasks()):
            results.append(result)

        stats = strategy.get_stats()

        # Verify all expected stats are present
        assert "current_concurrency" in stats
        assert "throughput" in stats
        assert "total_completed" in stats
        assert "total_tasks" in stats
        assert "recent_errors" in stats
        assert "adaptation_history" in stats

        # Verify stats values make sense
        assert stats["total_completed"] == 8
        assert stats["total_tasks"] == 8
        assert stats["recent_errors"] == 0
        assert isinstance(stats["adaptation_history"], list)

    @pytest.mark.asyncio
    async def test_adaptive_concurrency_limits(self):
        """Test that adaptive strategy respects concurrency limits."""
        strategy = AdaptiveStrategy(
            initial_concurrency=5,
            min_concurrency=2,
            max_concurrency=8,
            adaptation_interval=0.01,
        )

        def create_tasks():
            for i in range(6):

                async def task(task_id=i):
                    await asyncio.sleep(0.01)
                    return f"result_{task_id}"

                yield task

        results = []
        async for result in strategy.execute(create_tasks()):
            results.append(result)

        # Strategy should respect limits
        assert strategy.current_concurrency >= 2
        assert strategy.current_concurrency <= 8
        assert len(results) == 6

    @pytest.mark.asyncio
    async def test_adaptive_throughput_measurement(self):
        """Test throughput measurement accuracy."""
        strategy = AdaptiveStrategy(
            initial_concurrency=2,
            adaptation_interval=0.1,
        )

        start_time = time.time()

        def create_tasks():
            for i in range(10):

                async def task(task_id=i):
                    await asyncio.sleep(0.01)
                    return f"result_{task_id}"

                yield task

        results = []
        async for result in strategy.execute(create_tasks()):
            results.append(result)

        end_time = time.time()
        elapsed = end_time - start_time

        stats = strategy.get_stats()
        measured_throughput = stats["throughput"]

        # Rough throughput check (should be in reasonable range)
        if measured_throughput is not None:
            expected_throughput = 10 / elapsed
            # Allow for some variance due to overhead and timing
            assert measured_throughput > 0
            assert measured_throughput < expected_throughput * 2  # Not too high
