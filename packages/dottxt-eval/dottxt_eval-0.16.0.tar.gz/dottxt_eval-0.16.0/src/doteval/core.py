import asyncio
import functools
import itertools
from typing import Callable, Iterable, Optional

from tenacity import (
    AsyncRetrying,
    Retrying,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential_jitter,
)

from doteval.concurrency import AdaptiveStrategy, SequentialStrategy
from doteval.datasets.base import _registry
from doteval.models import EvaluationSummary, Record, Result
from doteval.progress import EvaluationProgress, get_dataset_info
from doteval.sessions import SessionManager
from doteval.storage import Storage

# Default retry configuration
DEFAULT_MAX_RETRIES = 3
DEFAULT_RETRY_DELAY = 1.0  # Initial delay in seconds
DEFAULT_MAX_DELAY = 30.0  # Maximum delay between retries

CONNECTION_ERRORS = (
    ConnectionError,
    ConnectionResetError,
    ConnectionAbortedError,
    ConnectionRefusedError,
    TimeoutError,
    OSError,
)


class ForEach:
    def __init__(
        self,
        retries: Optional[AsyncRetrying] = None,
        concurrency: Optional[object] = None,
        storage: Optional[Storage] = None,
    ):
        """Initialize ForEach decorator with optional configuration.

        Args:
            name: Optional name for the evaluation
            retries: Optional AsyncRetrying instance for retry configuration
            concurrency: Optional concurrency strategy
            storage: Optional storage backend
        """
        self.retries = retries
        self.concurrency = concurrency
        self.storage = storage

    def __call__(self, column_spec: str, dataset: Iterable):
        def core_foreach(column_spec: str, dataset: Iterable):
            """
            Decorator that marks a function for running against each item in a dataset.

            When used with `pytest`, the decorated function will be automatically
            executed against all dataset items as part of the evaluation suite.
            Functions decorated by `foreach` can also be executed as normal Python
            functions.

            The decorated function inherits retry, concurrency, and storage configuration
            from the ForEach instance that created it.

            Args:
                column_spec: Comma-separated list of column names
                dataset: An iterator of tuples or lists, each representing a row of data

            Returns:
                A decorated function that can be used as a regular function or as a `pytest` test

            """

            def decorator(eval_fn: Callable) -> Callable:
                if asyncio.iscoroutinefunction(eval_fn):
                    # Create async wrapper for async eval functions
                    @functools.wraps(eval_fn)
                    async def async_wrapper(
                        evaluation_name, experiment_name, samples, **kwargs
                    ):
                        return await run_evaluation(
                            eval_fn,
                            column_spec,
                            dataset,
                            evaluation_name,
                            experiment_name,
                            samples,
                            retries=self.retries,
                            concurrency=self.concurrency,
                            storage=self.storage,
                            **kwargs,
                        )

                    # Store parsed column names for plugin
                    async_wrapper._column_names = [col.strip() for col in column_spec.split(",")]  # type: ignore

                    return async_wrapper
                else:
                    # Create sync wrapper for sync eval functions
                    @functools.wraps(eval_fn)
                    def sync_wrapper(
                        evaluation_name, experiment_name, samples, **kwargs
                    ):
                        return run_evaluation(
                            eval_fn,
                            column_spec,
                            dataset,
                            evaluation_name,
                            experiment_name,
                            samples,
                            retries=self.retries,
                            concurrency=self.concurrency,
                            storage=self.storage,
                            **kwargs,
                        )

                    # Store parsed column names for plugin
                    sync_wrapper._column_names = [col.strip() for col in column_spec.split(",")]  # type: ignore

                    return sync_wrapper

            return decorator

        return core_foreach(column_spec, dataset)

    def __getattr__(self, dataset_name: str):
        def dataset_foreach(split: Optional[str] = None, **kwargs):
            dataset_class = _registry.get_dataset_class(dataset_name)
            dataset_instance = (
                dataset_class(split, **kwargs)
                if split is not None
                else dataset_class(**kwargs)
            )
            column_spec = ",".join(dataset_class.columns)

            def decorator(eval_fn: Callable):
                if asyncio.iscoroutinefunction(eval_fn):
                    # Create async wrapper for async eval functions
                    @functools.wraps(eval_fn)
                    async def async_wrapper(
                        evaluation_name, experiment_name, samples, **kwargs
                    ):
                        return await run_evaluation(
                            eval_fn,
                            column_spec,
                            dataset_instance,
                            evaluation_name,
                            experiment_name,
                            samples,
                            retries=self.retries,
                            concurrency=self.concurrency,
                            storage=self.storage,
                            **kwargs,
                        )

                    # Store parsed column names for plugin
                    async_wrapper._column_names = [col.strip() for col in column_spec.split(",")]  # type: ignore

                    return async_wrapper
                else:
                    # Create sync wrapper for sync eval functions
                    @functools.wraps(eval_fn)
                    def sync_wrapper(
                        evaluation_name, experiment_name, samples, **kwargs
                    ):
                        return run_evaluation(
                            eval_fn,
                            column_spec,
                            dataset_instance,
                            evaluation_name,
                            experiment_name,
                            samples,
                            retries=self.retries,
                            concurrency=self.concurrency,
                            storage=self.storage,
                            **kwargs,
                        )

                    # Store parsed column names for plugin
                    sync_wrapper._column_names = [col.strip() for col in column_spec.split(",")]  # type: ignore

                    return sync_wrapper

            decorator._dataset_name = dataset_name  # type: ignore
            decorator._split = split  # type: ignore
            return decorator

        return dataset_foreach


# Create default instance for backward compatibility
foreach = ForEach()


def run_evaluation(
    eval_fn: Callable,
    column_spec: str,
    dataset: Iterable,
    evaluation_name: str,
    experiment_name: Optional[str] = None,
    samples: Optional[int] = None,
    retries: Optional[AsyncRetrying] = None,
    concurrency: Optional[object] = None,
    storage: Optional[Storage] = None,
    **kwargs,
) -> EvaluationSummary:
    """
    Run an evaluation function against each item in a dataset.

    Args:
        eval_fn: The function to run for each dataset item
        column_spec: Comma-separated list of column names
        dataset: An iterator of tuples or lists, each representing a row of data
        experiment_name: Optional experiment name (used when creating SessionManager)
        evaluation_name: The name of the evaluation being run
        samples: Maximum number of dataset samples to evaluate (None for all)
        retries: Retry strategy (AsyncRetrying for async, Retrying for sync)
        concurrency: Concurrency strategy (AsyncConcurrencyStrategy or SyncConcurrencyStrategy)
        storage: Storage backend for results
        **kwargs: Additional arguments to pass to the evaluation function

    Returns:
        An EvaluationSummary containing all results

    """
    session_manager = SessionManager(storage=storage, experiment_name=experiment_name)

    session_manager.start_evaluation(evaluation_name)

    columns = [col.strip() for col in column_spec.split(",")]

    # Get dataset info for progress tracking
    dataset_info = get_dataset_info(dataset)

    # Adjust total count if samples parameter is specified
    if samples is not None and dataset_info.get("total_rows") is not None:
        dataset_info["total_rows"] = min(samples, dataset_info["total_rows"])

    # Batch remove from storage all the elements that errored out in the
    # previous run since we're going to re-try them.
    completed_ids: set[int] = set()
    items_to_retry: set[int] = set()
    if session_manager and session_manager.current_experiment:
        # Get successfully completed items
        completed_items = session_manager.storage.completed_items(
            session_manager.current_experiment, evaluation_name
        )
        completed_ids = set(completed_items)

        all_results = session_manager.storage.get_results(
            session_manager.current_experiment, evaluation_name
        )
        all_item_ids = {r.item_id for r in all_results}
        items_to_retry = all_item_ids - completed_ids

        if items_to_retry:
            session_manager.storage.remove_error_results_batch(
                session_manager.current_experiment,
                evaluation_name,
                list(items_to_retry),
            )

    dataset = (
        (item_id, row_data)
        for item_id, row_data in enumerate(dataset)
        if item_id not in completed_ids
    )

    dataset = itertools.islice(dataset, None, samples)

    # Run the evaluation
    try:
        if asyncio.iscoroutinefunction(eval_fn):
            result = _run_evaluation_async(
                evaluation_name,
                eval_fn,
                columns,
                dataset,
                concurrency,
                retries,
                session_manager,
                samples,
                dataset_info,
                storage,
                **kwargs,
            )
        else:
            result = _run_evaluation_sync(
                evaluation_name,
                eval_fn,
                columns,
                dataset,
                concurrency,
                retries,
                session_manager,
                samples,
                dataset_info,
                storage,
                **kwargs,
            )

        session_manager.finish_evaluation(evaluation_name, success=True)

        return result
    except Exception:
        session_manager.finish_evaluation(evaluation_name, success=False)
        raise


def _run_evaluation_sync(
    evaluation_name,
    eval_fn,
    columns,
    dataset,
    concurrency,
    retries,
    session_manager,
    samples,
    dataset_info,
    storage,
    **kwargs,
):
    """
    Run the evaluation when `eval_fn` is a Python function, against
    each item in the dataset.

    Args:
        evaluation_name: The name of the evaluation currently being run
        eval_fn: The function to run for each dataset item
        columns: List of column names that map to dataset fields
        dataset: An iterator of tuples or lists, each representing a row of data
        concurrency: Concurrency strategy for sync execution (defaults to SequentialStrategy)
        retries: Retry strategy for handling failures (defaults to Retrying with 3 attempts)
        samples: Maximum number of samples to evaluate
        dataset_info: Optional dataset information (name, split, size)
        session_manager: The current session's session manager
        storage: Storage backend for results (defaults to JSONStorage)
        **kwargs: Additional arguments to pass to the evaluation function

    Returns:
        An EvaluationSummary containing all results

    """
    # Set default concurrency strategy if not provided
    if concurrency is None:
        concurrency = SequentialStrategy()

    # Set default retry strategy if not provided
    if retries is None:
        sync_retries = Retrying(
            retry=retry_if_exception_type(CONNECTION_ERRORS),
            stop=stop_after_attempt(DEFAULT_MAX_RETRIES),
            wait=wait_exponential_jitter(
                initial=DEFAULT_RETRY_DELAY, max=DEFAULT_MAX_DELAY
            ),
            reraise=True,
        )
    else:
        sync_retries = retries

    # Create tasks iterator
    def create_tasks():
        for item_id, row_data in dataset:
            row_dict = {col: data for col, data in zip(columns, row_data)}

            def task(item_id=item_id, row_dict=row_dict):
                try:
                    # Apply retry logic
                    wrapped_fn = sync_retries.wraps(eval_fn)
                    sample = wrapped_fn(**row_dict, **kwargs)

                    if not isinstance(sample, Result):
                        raise ValueError(
                            "Evaluation functions must return a Result object"
                        )

                    # Check if the Result contains an error and propagate it to Record
                    if sample.error is not None:
                        return Record(sample, item_id, row_dict, sample.error)
                    else:
                        return Record(sample, item_id, row_dict)
                except Exception as e:
                    # Create a Result with False scores for error cases
                    error_result = Result(prompt="")
                    error_msg = f"{type(e).__name__}: {str(e)}"
                    return Record(error_result, item_id, row_dict, error_msg)

            yield task

    with EvaluationProgress(evaluation_name, dataset_info) as progress:
        for result in concurrency.execute(
            create_tasks(), progress_callback=progress.update_progress
        ):
            session_manager.add_results(evaluation_name, [result])

    results = session_manager.get_results(evaluation_name)

    return EvaluationSummary(results)


async def _run_evaluation_async(
    evaluation_name,
    eval_fn,
    columns,
    dataset,
    concurrency,
    retries,
    session_manager,
    samples,
    dataset_info,
    storage,
    **kwargs,
):
    """
    Run the evaluation when `eval_fn` is a coroutine, against each item in the
    dataset.

    Args:
        evaluation_name: The name of the current evaluation
        eval_fn: The function to run for each dataset item
        columns: List of column names that map to dataset fields
        dataset: An iterator of tuples or lists, each representing a row of data
        concurrency: Concurrency strategy for async execution (defaults to SlidingWindowStrategy)
        retries: Retry strategy for handling failures (defaults to AsyncRetrying with connection error handling)
        samples: Maximum number of samples to evaluate
        dataset_info: Optional dataset information (name, split, size)
        session_manager: The current session's session manager
        samples: Maximum number of dataset samples to evaluate (None for all)
        storage: Storage backend for results (defaults to JSONStorage)
        **kwargs: Additional arguments to pass to the evaluation function

    Returns:
        An EvaluationSummary containing all results

    """

    # Set default concurrency strategy if not provided
    if concurrency is None:
        concurrency = AdaptiveStrategy()

    # Set default retry strategy if not provided
    if retries is None:
        retries = AsyncRetrying(
            retry=retry_if_exception_type(CONNECTION_ERRORS),
            stop=stop_after_attempt(DEFAULT_MAX_RETRIES),
            wait=wait_exponential_jitter(
                initial=DEFAULT_RETRY_DELAY, max=DEFAULT_MAX_DELAY
            ),
        )

    # Create async tasks iterator
    def create_tasks():
        for item_id, row_data in dataset:
            row_dict = {col: data for col, data in zip(columns, row_data)}

            async def task(item_id=item_id, row_dict=row_dict):
                try:
                    # Apply retry logic
                    wrapped_fn = retries.wraps(eval_fn)
                    sample = await wrapped_fn(**row_dict, **kwargs)

                    if not isinstance(sample, Result):
                        raise ValueError(
                            "Evaluation functions must return a Result object"
                        )

                    # Check if the Result contains an error and propagate it to Record
                    if sample.error is not None:
                        return Record(sample, item_id, row_dict, sample.error)
                    else:
                        return Record(sample, item_id, row_dict)
                except Exception as e:
                    # Create empty Result for error cases
                    empty_result = Result(prompt="")
                    error_msg = f"{type(e).__name__}: {str(e)}"
                    return Record(empty_result, item_id, row_dict, error_msg)

            yield task

    with EvaluationProgress(
        evaluation_name, dataset_info, show_individual_tasks=True
    ) as progress:
        # Execute tasks using the concurrency strategy
        async for result in concurrency.execute(
            create_tasks(), progress_callback=progress.update_progress
        ):
            session_manager.add_results(evaluation_name, [result])

    results = session_manager.get_results(evaluation_name)

    return EvaluationSummary(results)
