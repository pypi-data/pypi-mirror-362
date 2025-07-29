"""Sequential execution strategy for sync functions."""

from typing import Callable, Iterator, TypeVar

T = TypeVar("T")


class SequentialStrategy:
    """Sequential execution for sync functions."""

    def execute(
        self,
        tasks: Iterator[Callable[[], T]],
        progress_callback: Callable[[T], None] | None = None,
    ) -> Iterator[T]:
        """Execute sync tasks sequentially.

        Args:
            tasks: An iterator of callables that return results
            progress_callback: Optional callback to report progress

        Yields:
            Results from executing the tasks
        """
        for task in tasks:
            result = task()
            if progress_callback:
                progress_callback(result)
            yield result
