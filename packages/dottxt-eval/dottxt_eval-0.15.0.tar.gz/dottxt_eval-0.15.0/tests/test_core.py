import asyncio
import tempfile

import pytest

from doteval.core import ForEach, run_evaluation
from doteval.evaluators import evaluator, exact_match
from doteval.metrics import accuracy, metric, registry
from doteval.models import Result
from doteval.sessions import SessionManager


@pytest.fixture
def dataset():
    s1 = ("What is the first letter in the alphabet?", "a")
    s2 = ("What is the second letter in the alphabet?", "b")
    return [s1, s2]


def create_isolated_foreach():
    """Create ForEach instance with isolated storage for testing."""
    import tempfile

    temp_dir = tempfile.mkdtemp()
    return ForEach(storage=f"json://{temp_dir}")


@pytest.fixture
def session_manager():
    with tempfile.TemporaryDirectory() as temp_dir:
        yield SessionManager(storage=f"json://{temp_dir}", experiment_name="test_exp")


@metric
def metric_any():
    def metric(scores: list[bool]) -> bool:
        return any(scores)

    return metric


# Register the custom metric
registry["metric_any"] = metric_any()


def test_foreach_sync_simple(dataset):
    import tempfile

    with tempfile.TemporaryDirectory() as temp_dir:
        # Create ForEach instance with isolated storage
        foreach_instance = ForEach(storage=f"json://{temp_dir}")

        @foreach_instance("question,answer", dataset)
        def eval_dummy(question, answer):
            prompt = f"Q: {question}"
            does_match = exact_match(answer, "a")
            return Result(does_match, prompt=prompt)

        result = eval_dummy(
            evaluation_name="test_eval", experiment_name="test_exp", samples=None
        )
    assert isinstance(result.summary, dict)
    assert result.summary["exact_match"]["accuracy"] == 0.5


@pytest.mark.asyncio
async def test_foreach_async_simple(dataset):
    import tempfile

    with tempfile.TemporaryDirectory() as temp_dir:
        # Create ForEach instance with isolated storage
        foreach_instance = ForEach(storage=f"json://{temp_dir}")

        @foreach_instance("question,answer", dataset)
        async def eval_dummy(question, answer):
            await asyncio.sleep(0.001)
            prompt = f"Q: {question}"
            does_match = exact_match(answer, "a")
            print(question, answer, does_match)
            return Result(does_match, prompt=prompt)

        result = await eval_dummy(
            evaluation_name="test_eval", experiment_name="test_exp", samples=None
        )
    assert isinstance(result.summary, dict)
    assert result.summary["exact_match"]["accuracy"] == 0.5


def test_foreach_sync_two_metric(dataset):
    import tempfile

    with tempfile.TemporaryDirectory() as temp_dir:
        # Create ForEach instance with isolated storage
        foreach_instance = ForEach(storage=f"json://{temp_dir}")

        @evaluator(metrics=[accuracy(), metric_any()])
        def dummy_match(answer, target):
            return answer == target

        @foreach_instance("question,answer", dataset)
        def eval_dummy(question, answer):
            prompt = f"Q: {question}"
            does_match = dummy_match(answer, "a")
            return Result(does_match, prompt=prompt)

        result = eval_dummy(
            evaluation_name="test_eval", experiment_name="test_exp", samples=None
        )
    assert isinstance(result.summary, dict)
    assert result.summary["dummy_match"]["accuracy"] == 0.5
    assert result.summary["dummy_match"]["metric_any"] is True


@pytest.mark.asyncio
async def test_foreach_async_two_metric(dataset):
    import tempfile

    with tempfile.TemporaryDirectory() as temp_dir:
        # Create ForEach instance with isolated storage
        foreach_instance = ForEach(storage=f"json://{temp_dir}")

        @evaluator(metrics=[accuracy(), metric_any()])
        def dummy_match(answer, target):
            return answer == target

        @foreach_instance("question,answer", dataset)
        async def eval_dummy(question, answer):
            await asyncio.sleep(0.001)
            prompt = f"Q: {question}"
            does_match = dummy_match(answer, "a")
            return Result(does_match, prompt=prompt)

        result = await eval_dummy(
            evaluation_name="test_eval", experiment_name="test_exp", samples=None
        )
    assert isinstance(result.summary, dict)
    assert result.summary["dummy_match"]["accuracy"] == 0.5
    assert result.summary["dummy_match"]["metric_any"] is True


def test_foreach_sync_two_evaluators(dataset):
    import tempfile

    with tempfile.TemporaryDirectory() as temp_dir:
        # Create ForEach instance with isolated storage
        foreach_instance = ForEach(storage=f"json://{temp_dir}")

        @evaluator(metrics=[accuracy()])
        def mismatch(answer, target):
            return answer != target

        @foreach_instance("question,answer", dataset)
        def eval_dummy(question, answer):
            prompt = f"Q: {question}"
            does_match = exact_match(answer, "a")
            does_mismatch = mismatch(answer, "b")
            return Result(does_match, does_mismatch, prompt=prompt)

        result = eval_dummy(
            evaluation_name="test_eval", experiment_name="test_exp", samples=None
        )
    assert isinstance(result.summary, dict)
    assert result.summary["exact_match"]["accuracy"] == 0.5
    assert result.summary["mismatch"]["accuracy"] == 0.5


@pytest.mark.asyncio
async def test_foreach_async_two_evaluators(dataset):
    import tempfile

    with tempfile.TemporaryDirectory() as temp_dir:
        # Create ForEach instance with isolated storage
        foreach_instance = ForEach(storage=f"json://{temp_dir}")

        @evaluator(metrics=[accuracy()])
        def mismatch(answer, target):
            return answer != target

        @foreach_instance("question,answer", dataset)
        async def eval_dummy(question, answer):
            await asyncio.sleep(0.001)
            prompt = f"Q: {question}"
            does_match = exact_match(answer, "a")
            does_mismatch = mismatch(answer, "b")
            return Result(does_match, does_mismatch, prompt=prompt)

        result = await eval_dummy(
            evaluation_name="test_eval", experiment_name="test_exp", samples=None
        )
    assert isinstance(result.summary, dict)
    assert result.summary["exact_match"]["accuracy"] == 0.5
    assert result.summary["mismatch"]["accuracy"] == 0.5


@pytest.fixture
def large_dataset():
    """Fixture with larger dataset for testing samples."""
    return [
        ("Question 1", "Answer 1"),
        ("Question 2", "Answer 2"),
        ("Question 3", "Answer 3"),
        ("Question 4", "Answer 4"),
        ("Question 5", "Answer 5"),
    ]


def test_foreach_sync_samples_parameter(large_dataset):
    """Test the samples parameter when calling function directly."""
    import tempfile

    with tempfile.TemporaryDirectory() as temp_dir:
        # Create ForEach instance with isolated storage
        foreach_instance = ForEach(storage=f"json://{temp_dir}")

        @foreach_instance("question,answer", large_dataset)
        def eval_samples(question, answer):
            prompt = f"Q: {question}"
            return Result(exact_match(question, answer), prompt=prompt)

        # Test without samples limit
        result_all = eval_samples(
            evaluation_name="test_eval", experiment_name="test_exp", samples=None
        )
        assert len(result_all.results) == 5

        # Test with samples limit
        result_limited = eval_samples(
            evaluation_name="test_eval", experiment_name="test_exp2", samples=2
        )
        assert len(result_limited.results) == 2

        # Verify the correct samples were processed
        assert result_limited.results[0].dataset_row["question"] == "Question 1"
        assert result_limited.results[1].dataset_row["question"] == "Question 2"


@pytest.mark.asyncio
async def test_foreach_async_samples_parameter(large_dataset):
    """Test the samples parameter when calling function directly."""
    import tempfile

    with tempfile.TemporaryDirectory() as temp_dir:
        # Create ForEach instance with isolated storage
        foreach_instance = ForEach(storage=f"json://{temp_dir}")

        @foreach_instance("question,answer", large_dataset)
        async def eval_samples(question, answer):
            await asyncio.sleep(0.001)
            prompt = f"Q: {question}"
            return Result(exact_match(question, answer), prompt=prompt)

        # Test without samples limit
        result_all = await eval_samples(
            evaluation_name="test_eval", experiment_name="test_exp", samples=None
        )
        assert len(result_all.results) == 5

        # Test with samples limit
        result_limited = await eval_samples(
            evaluation_name="test_eval", experiment_name="test_exp2", samples=2
        )
        assert len(result_limited.results) == 2

        # Verify the correct samples were processed
        assert result_limited.results[0].dataset_row["question"] in [
            "Question 1",
            "Question 2",
        ]
        assert result_limited.results[1].dataset_row["question"] in [
            "Question 1",
            "Question 2",
        ]


def test_foreach_sync_samples_with_additional_kwargs(large_dataset):
    """Test that samples works alongside other kwargs."""
    import tempfile

    with tempfile.TemporaryDirectory() as temp_dir:
        # Create ForEach instance with isolated storage
        foreach_instance = ForEach(storage=f"json://{temp_dir}")

        @foreach_instance("question,answer", large_dataset)
        def eval_with_kwargs(question, answer, extra_param=None):
            # Use the extra parameter in some way
            if extra_param:
                result = f"{question}-{extra_param}"
                expected = f"{question}-test"
            else:
                result = question
                expected = answer
            return exact_match(result, expected)

        # Test with samples and extra kwargs
        result = eval_with_kwargs(
            evaluation_name="test_eval",
            experiment_name="test_exp",
            samples=2,
            extra_param="test",
        )
        assert len(result.results) == 2


@pytest.mark.asyncio
async def test_foreach_async_samples_with_additional_kwargs(large_dataset):
    """Test that samples works alongside other kwargs."""
    import tempfile

    with tempfile.TemporaryDirectory() as temp_dir:
        # Create ForEach instance with isolated storage
        foreach_instance = ForEach(storage=f"json://{temp_dir}")

        @foreach_instance("question,answer", large_dataset)
        async def eval_with_kwargs(question, answer, extra_param=None):
            # Use the extra parameter in some way
            await asyncio.sleep(0.001)
            if extra_param:
                result = f"{question}-{extra_param}"
                expected = f"{question}-test"
            else:
                result = question
                expected = answer
            return exact_match(result, expected)

        # Test with samples and extra kwargs
        result = await eval_with_kwargs(
            evaluation_name="test_eval",
            experiment_name="test_exp",
            samples=2,
            extra_param="test",
        )
        assert len(result.results) == 2


def test_foreach_sync_zero_samples(large_dataset):
    """Test samples=0 behavior."""
    import tempfile

    with tempfile.TemporaryDirectory() as temp_dir:
        # Create ForEach instance with isolated storage
        foreach_instance = ForEach(storage=f"json://{temp_dir}")

        @foreach_instance("question,answer", large_dataset)
        def eval_zero_samples(question, answer):
            return exact_match(question, answer)

        result = eval_zero_samples(
            evaluation_name="test_eval", experiment_name="test_exp", samples=0
        )
        assert len(result.results) == 0


@pytest.mark.asyncio
async def test_foreach_async_zero_samples(large_dataset):
    """Test samples=0 behavior."""
    import tempfile

    with tempfile.TemporaryDirectory() as temp_dir:
        # Create ForEach instance with isolated storage
        foreach_instance = ForEach(storage=f"json://{temp_dir}")

        @foreach_instance("question,answer", large_dataset)
        async def eval_zero_samples(question, answer):
            await asyncio.sleep(0.001)
            return exact_match(question, answer)

        result = await eval_zero_samples(
            evaluation_name="test_eval", experiment_name="test_exp", samples=0
        )
        assert len(result.results) == 0


def test_foreach_sync_samples_larger_than_dataset(large_dataset):
    """Test samples larger than dataset size."""
    import tempfile

    with tempfile.TemporaryDirectory() as temp_dir:
        # Create ForEach instance with isolated storage
        foreach_instance = ForEach(storage=f"json://{temp_dir}")

        @foreach_instance("question,answer", large_dataset)
        def eval_large_samples(question, answer):
            return exact_match(question, answer)

        result = eval_large_samples(
            evaluation_name="test_eval", experiment_name="test_exp", samples=10
        )
        assert len(result.results) == 5  # Should only process available samples


@pytest.mark.asyncio
async def test_foreach_async_samples_larger_than_dataset(large_dataset):
    """Test samples larger than dataset size."""
    import tempfile

    with tempfile.TemporaryDirectory() as temp_dir:
        # Create ForEach instance with isolated storage
        foreach_instance = ForEach(storage=f"json://{temp_dir}")

        @foreach_instance("question,answer", large_dataset)
        async def eval_large_samples(question, answer):
            await asyncio.sleep(0.001)
            return exact_match(question, answer)

        result = await eval_large_samples(
            evaluation_name="test_eval", experiment_name="test_exp", samples=10
        )
        assert len(result.results) == 5  # Should only process available samples


def test_foreach_sync_run_evaluation_samples(large_dataset):
    """Test calling run_evaluation directly with samples parameter."""
    import tempfile

    with tempfile.TemporaryDirectory() as temp_dir:
        storage_path = f"json://{temp_dir}"

        def simple_eval(question, answer):
            prompt = f"Q: {question}"
            return Result(exact_match(question, answer), prompt=prompt)

        # Test run_evaluation directly
        result = run_evaluation(
            simple_eval,
            "question,answer",
            large_dataset,
            "test_eval",
            experiment_name="test_exp",
            samples=2,
            storage=storage_path,
        )
        assert len(result.results) == 2
        assert result.results[0].dataset_row["question"] == "Question 1"
        assert result.results[1].dataset_row["question"] == "Question 2"

        # Test without samples
        result_full = run_evaluation(
            simple_eval,
            "question,answer",
            large_dataset,
            "test_eval",
            experiment_name="test_exp2",
            samples=None,
            storage=storage_path,
        )
        assert len(result_full.results) == 5


def test_foreach_sync_samples_order(large_dataset):
    """Test that samples parameter works consistently across different call methods."""
    import tempfile

    with tempfile.TemporaryDirectory() as temp_dir:
        # Create ForEach instance with isolated storage
        foreach_instance = ForEach(storage=f"json://{temp_dir}")

        @foreach_instance("question,answer", large_dataset)
        def eval_consistency(question, answer):
            prompt = f"Q: {question}"
            return Result(exact_match(question, answer), prompt=prompt)

        # Test different sample sizes
        for sample_size in [1, 2, 3, 5]:
            result = eval_consistency(
                evaluation_name="test_eval",
                experiment_name=f"test_exp_{sample_size}",
                samples=sample_size,
            )
            assert len(result.results) == sample_size

            # Verify correct samples were processed (should be first N)
            for i in range(sample_size):
                expected_question = f"Question {i + 1}"
                actual_question = result.results[i].dataset_row["question"]
                assert actual_question == expected_question


@pytest.mark.asyncio
async def test_foreach_async_samples_order(large_dataset):
    """Test that samples parameter works consistently across different call methods."""
    import tempfile

    with tempfile.TemporaryDirectory() as temp_dir:
        # Create ForEach instance with isolated storage
        foreach_instance = ForEach(storage=f"json://{temp_dir}")

        @foreach_instance("question,answer", large_dataset)
        async def eval_consistency(question, answer):
            await asyncio.sleep(0.001)
            return exact_match(question, answer)

        # Test different sample sizes
        for sample_size in [1, 2, 3, 5]:
            result = await eval_consistency(
                evaluation_name="test_eval",
                experiment_name=f"test_exp_{sample_size}",
                samples=sample_size,
            )
            assert len(result.results) == sample_size

            # Verify correct samples were processed (should be first N)
            expected_questions = [f"Question {n + 1}" for n in range(sample_size)]
            for i in range(sample_size):
                actual_question = result.results[i].dataset_row["question"]
                assert actual_question in expected_questions


def test_foreach_sync_empty_dataset():
    """Test behavior with empty dataset."""
    import tempfile

    with tempfile.TemporaryDirectory() as temp_dir:
        # Create ForEach instance with isolated storage
        foreach_instance = ForEach(storage=f"json://{temp_dir}")

        dataset = []

        @foreach_instance("question,answer", dataset)
        def eval_empty(question, answer):
            return exact_match(question, answer)

        result = eval_empty(
            evaluation_name="test_eval", experiment_name="test_exp", samples=None
        )
        assert len(result.results) == 0


@pytest.mark.asyncio
async def test_foreach_async_empty_dataset():
    """Test behavior with empty dataset."""
    import tempfile

    with tempfile.TemporaryDirectory() as temp_dir:
        # Create ForEach instance with isolated storage
        foreach_instance = ForEach(storage=f"json://{temp_dir}")

        dataset = []

        @foreach_instance("question,answer", dataset)
        async def eval_empty(question, answer):
            await asyncio.sleep(0.001)
            return exact_match(question, answer)

        result = await eval_empty(
            evaluation_name="test_eval", experiment_name="test_exp", samples=None
        )
        assert len(result.results) == 0


def test_foreach_sync_single_column():
    """Test with a single column dataset."""
    import tempfile

    with tempfile.TemporaryDirectory() as temp_dir:
        # Create ForEach instance with isolated storage
        foreach_instance = ForEach(storage=f"json://{temp_dir}")

        dataset = [("item1",), ("item2",), ("item3",)]

        @foreach_instance("item", dataset)
        def eval_single_column(item):
            return exact_match(item, item)  # Always matches it

        result = eval_single_column(
            evaluation_name="test_eval", experiment_name="test_exp", samples=None
        )
        assert len(result.results) == 3
        for i, eval_result in enumerate(result.results):
            assert eval_result.dataset_row["item"] == f"item{i + 1}"


@pytest.mark.asyncio
async def test_foreach_async_single_column():
    """Test with a single column dataset."""
    import tempfile

    with tempfile.TemporaryDirectory() as temp_dir:
        # Create ForEach instance with isolated storage
        foreach_instance = ForEach(storage=f"json://{temp_dir}")

        dataset = [("item1",), ("item2",), ("item3",)]

        @foreach_instance("item", dataset)
        async def eval_single_column(item):
            await asyncio.sleep(0.001)
            return exact_match(item, item)  # Always matches it

        result = await eval_single_column(
            evaluation_name="test_eval", experiment_name="test_exp", samples=None
        )
        assert len(result.results) == 3
        expected_items = [f"item{i + 1}" for i in range(len(result.results))]
        for i, eval_result in enumerate(result.results):
            assert eval_result.dataset_row["item"] in expected_items


def test_foreach_sync_many_columns():
    """Test with many columns."""
    import tempfile

    with tempfile.TemporaryDirectory() as temp_dir:
        # Create ForEach instance with isolated storage
        foreach_instance = ForEach(storage=f"json://{temp_dir}")

        dataset = [("a", "b", "c", "d", "e"), ("f", "g", "h", "i", "j")]

        @foreach_instance("col1,col2,col3,col4,col5", dataset)
        def eval_many_columns(col1, col2, col3, col4, col5):
            combined = f"{col1}{col2}{col3}{col4}{col5}"
            return exact_match(combined, combined)  # Always matches

        result = eval_many_columns(
            evaluation_name="test_eval", experiment_name="test_exp", samples=None
        )
        assert len(result.results) == 2

        # Verify all columns are present
        first_result = result.results[0]
        assert first_result.dataset_row["col1"] == "a"
        assert first_result.dataset_row["col5"] == "e"


@pytest.mark.asyncio
async def test_foreach_async_many_columns():
    """Test with many columns."""
    import tempfile

    with tempfile.TemporaryDirectory() as temp_dir:
        # Create ForEach instance with isolated storage
        foreach_instance = ForEach(storage=f"json://{temp_dir}")

        dataset = [("a", "b", "c", "d", "e"), ("f", "g", "h", "i", "j")]

        @foreach_instance("col1,col2,col3,col4,col5", dataset)
        async def eval_many_columns(col1, col2, col3, col4, col5):
            await asyncio.sleep(0.001)
            combined = f"{col1}{col2}{col3}{col4}{col5}"
            return exact_match(combined, combined)  # Always matches

        result = await eval_many_columns(
            evaluation_name="test_eval", experiment_name="test_exp", samples=None
        )
        assert len(result.results) == 2

        # Verify all columns are present
        first_result = result.results[0]
        assert first_result.dataset_row["col1"] in ["a", "f"]
        assert first_result.dataset_row["col5"] in ["e", "j"]


# Additional tests to increase core.py coverage are included above


def test_async_foreach_with_retry_parameters():
    """Test async foreach evaluation runs successfully."""
    import tempfile

    with tempfile.TemporaryDirectory() as temp_dir:
        # Create ForEach instance with isolated storage
        foreach_instance = ForEach(storage=f"json://{temp_dir}")

        dataset = [("test1", "answer1"), ("test2", "answer2")]

        call_count = 0

        @foreach_instance("input,expected", dataset)
        async def async_eval_with_retry(input, expected):
            nonlocal call_count
            call_count += 1
            # Simulate an async operation
            await asyncio.sleep(0.001)
            return Result(prompt=f"Q: {input}")

        # Run the evaluation
        result = asyncio.run(
            async_eval_with_retry(
                evaluation_name="test_eval", experiment_name="test_exp", samples=None
            )
        )

        assert len(result.results) == 2
        assert call_count == 2


def test_async_evaluation_without_retry():
    """Test async evaluation when max_retries is 0."""
    import tempfile

    with tempfile.TemporaryDirectory() as temp_dir:
        # Create ForEach instance with isolated storage
        foreach_instance = ForEach(storage=f"json://{temp_dir}")

        dataset = [("test1", "answer1")]

        @foreach_instance("input,expected", dataset)
        async def async_eval_no_retry(input, expected):
            await asyncio.sleep(0.001)
            return Result(prompt=f"Q: {input}")

        # Run with max_retries=0
        result = asyncio.run(
            async_eval_no_retry(
                evaluation_name="test_eval",
                experiment_name="test_exp",
                samples=None,
                max_retries=0,  # No retries
            )
        )

        assert len(result.results) == 1


def test_async_evaluation_with_exceptions():
    """Test that exceptions in async evaluation are captured as errors."""
    import tempfile

    with tempfile.TemporaryDirectory() as temp_dir:
        storage_path = f"json://{temp_dir}"

        dataset = [(f"test{i}", f"answer{i}") for i in range(5)]

        processed_items = []

        async def eval_fn_with_errors(**kwargs):
            """Evaluation function that may fail on some items."""
            item_id = kwargs.get("input", "").replace("test", "")

            # First and third items raise exceptions
            if item_id in ["0", "2"]:
                raise ValueError(f"Error on item {item_id}")

            # Other items process normally
            await asyncio.sleep(0.01)
            processed_items.append(item_id)
            return Result(prompt=f"Q: {kwargs['input']}")

        # The current implementation catches exceptions and stores them as errors
        column_spec = "input,expected"
        result = asyncio.run(
            run_evaluation(
                eval_fn_with_errors,
                column_spec,
                dataset,
                "test_eval",
                experiment_name="test_exp",
                samples=None,
                storage=storage_path,
                max_concurrency=5,
            )
        )

        # Check that errors were captured
        error_results = [r for r in result.results if r.error]
        assert len(error_results) == 2
        assert any("Error on item 0" in r.error for r in error_results)
        assert any("Error on item 2" in r.error for r in error_results)

        # Other items should have been processed
        assert len(processed_items) == 3  # Items 1, 3, 4 were processed


def test_sync_foreach_with_retry_parameters():
    """Test sync foreach evaluation with custom retry parameters."""
    import tempfile

    with tempfile.TemporaryDirectory() as temp_dir:
        # Create ForEach instance with isolated storage
        foreach_instance = ForEach(storage=f"json://{temp_dir}")

        dataset = [("test1", "answer1"), ("test2", "answer2")]

        @foreach_instance("input,expected", dataset)
        def sync_eval_with_retry(input, expected):
            return Result(prompt=f"Q: {input}")

        # Run with custom retry parameters
        result = sync_eval_with_retry(
            evaluation_name="test_eval",
            experiment_name="test_exp",
            samples=None,
            max_retries=3,
            retry_delay=1.5,
        )

        assert len(result.results) == 2


def test_evaluation_with_session_manager():
    """Test evaluation with session manager."""
    import tempfile

    with tempfile.TemporaryDirectory() as temp_dir:
        # Create ForEach instance with isolated storage
        foreach_instance = ForEach(storage=f"json://{temp_dir}")

        dataset = [("test1", "answer1"), ("test2", "answer2")]

        @foreach_instance("input,expected", dataset)
        def eval_with_session(input, expected):
            return Result(prompt=f"Q: {input}")

        result = eval_with_session(
            evaluation_name="test_eval", experiment_name="test_exp", samples=None
        )
        assert len(result.results) == 2


@pytest.mark.asyncio
async def test_async_evaluation_with_session_manager():
    """Test async evaluation with session manager."""
    import tempfile

    with tempfile.TemporaryDirectory() as temp_dir:
        # Create ForEach instance with isolated storage
        foreach_instance = ForEach(storage=f"json://{temp_dir}")

        dataset = [("test1", "answer1"), ("test2", "answer2")]

        @foreach_instance("input,expected", dataset)
        async def async_eval_with_session(input, expected):
            await asyncio.sleep(0.001)
            return Result(prompt=f"Q: {input}")

        result = await async_eval_with_session(
            evaluation_name="test_eval", experiment_name="test_exp", samples=None
        )
        assert len(result.results) == 2
