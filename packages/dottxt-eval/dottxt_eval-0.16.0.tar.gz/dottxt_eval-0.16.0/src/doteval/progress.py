import sys
from typing import Any, Dict, Optional

from rich.console import Console
from rich.live import Live
from rich.progress import (
    BarColumn,
    MofNCompleteColumn,
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
)
from rich.table import Table
from rich.text import Text

from doteval.models import Record


def _is_running_under_pytest() -> bool:
    """Check if we're currently running under pytest with progress enabled"""
    return "pytest" in sys.modules


def get_dataset_info(dataset):
    """Extract dataset information for progress display"""
    info = {"name": "Dataset", "total_rows": None}

    # Check if this is a Dataset instance from the registry
    if hasattr(dataset, "name") and hasattr(dataset, "num_rows"):
        info.update(
            {
                "name": dataset.name.upper(),
                "total_rows": dataset.num_rows,
            }
        )
    # Fallback to size estimation for direct iterators
    elif hasattr(dataset, "__len__"):
        try:
            info["total_rows"] = len(dataset)
        except (TypeError, AttributeError):
            pass

    return info


class EvaluationProgress:
    """Context manager for displaying progress bars during evaluations"""

    def __init__(
        self, test_name: str, dataset_info: dict, show_individual_tasks: bool = False
    ):
        self.test_name = test_name
        self.dataset_info = dataset_info
        self.show_individual_tasks = show_individual_tasks
        self.console = Console()
        self.live = None
        self.progress = None
        self.main_task = None
        self.active_tasks: Dict[int, str] = {}
        self.completed_count = 0
        self.total_count = dataset_info.get("total_rows")
        self.metrics: Dict[str, Any] = {}
        self.error_count = 0

    def __enter__(self):
        if not _is_running_under_pytest():
            return self

        # Create progress display
        if self.total_count:
            # Known size - use progress bar
            self.progress = Progress(
                TextColumn("✨ {task.description}"),
                BarColumn(bar_width=60),
                MofNCompleteColumn(),
                TextColumn("• Elapsed:"),
                TimeElapsedColumn(),
                TextColumn("• ETA:"),
                TimeRemainingColumn(),
                console=self.console,
                expand=False,
            )
            dataset_name = self.dataset_info.get("name", "Dataset")
            description = f"{dataset_name} [{self.total_count:,} examples]"
            self.main_task = self.progress.add_task(description, total=self.total_count)
        else:
            # Unknown size - use spinner
            self.progress = Progress(
                SpinnerColumn(),
                TextColumn("✨ {task.description}"),
                TextColumn("• {task.completed:,} completed"),
                TimeElapsedColumn(),
                console=self.console,
                expand=False,
            )
            dataset_name = self.dataset_info.get("name", "Dataset")
            description = f"{dataset_name} Evaluation"
            self.main_task = self.progress.add_task(description, total=None)

        self.live = Live(
            self._build_display(), console=self.console, refresh_per_second=4
        )
        self.live.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.live:
            self.live.stop()

    def _build_display(self):
        """Build the complete display with progress and metrics"""
        if not self.progress:
            return ""

        table = Table.grid(padding=(0, 0))
        table.add_column()

        # Add main progress
        table.add_row(self.progress)

        # Add metrics row if we have any (excluding errors)
        if self.metrics:
            metrics_parts = []

            # Add computed metrics
            for name, value in self.metrics.items():
                if isinstance(value, float):
                    metrics_parts.append(f"{name}: {value:.1%}")
                else:
                    metrics_parts.append(f"{name}: {value}")

            if metrics_parts:
                metrics_text = " • ".join(metrics_parts)
                table.add_row(Text(metrics_text, style="dim"))

        # Add errors on a separate line if any
        if self.error_count > 0:
            error_text = f"! {self.error_count} error{'s' if self.error_count != 1 else ''} encountered"
            table.add_row(Text(error_text, style="bold red"))

        return table

    def update_progress(self, result: Record):
        """Update progress with a new result"""
        if not self.progress:
            return

        self.completed_count += 1

        # Track errors
        if result.error is not None:
            self.error_count += 1

        # Calculate live metrics from scores
        self._update_metrics(result)

        # Update main progress
        if self.total_count:
            self.progress.update(self.main_task, completed=self.completed_count)
        else:
            self.progress.update(self.main_task, completed=self.completed_count)

        # Update live display
        if self.live:
            self.live.update(self._build_display())

    def _update_metrics(self, result: Record):
        """Calculate live metrics from evaluation results"""
        from collections import defaultdict

        # Group all results by evaluator and metric for calculation
        if not hasattr(self, "_all_results"):
            self._all_results = []
        self._all_results.append(result)

        # First pass: determine the expected score structure from successful results
        expected_scores = []
        for res in self._all_results:
            if res.error is None and res.result.scores:
                expected_scores = [
                    (score.name, score.metrics) for score in res.result.scores
                ]
                break

        # Recalculate metrics from all results so far
        aggregated_results: Dict[str, Dict[Any, Any]] = defaultdict(
            lambda: defaultdict(list)
        )
        for res in self._all_results:
            if res.error is not None:
                # For error cases, add False values for each expected score
                for score_name, metrics in expected_scores:
                    for metric in metrics:
                        aggregated_results[score_name][metric].append(False)
            else:
                # For successful cases, use actual scores
                for score in res.result.scores:
                    for metric in score.metrics:
                        aggregated_results[score.name][metric].append(score.value)

        # Compute and store metrics
        computed_metrics = {}
        for evaluator_name, metrics_values in aggregated_results.items():
            for metric_func, values in metrics_values.items():
                if values:  # Only compute if we have values
                    metric_name = metric_func.__name__.replace("_", " ").title()
                    computed_metrics[metric_name] = metric_func(values)

        self.metrics = computed_metrics

    def update_metrics(self, metrics: dict):
        """Update the metrics display"""
        self.metrics.update(metrics)
        if self.live:
            self.live.update(self._build_display())

    def add_task(self, description: str, total: Optional[int] = None):
        """Add an individual task (for async operations)"""
        if not self.progress or not self.show_individual_tasks:
            return None
        return self.progress.add_task(description, total=total)

    def update_task(self, task_id, **kwargs):
        """Update an individual task"""
        if self.progress and task_id is not None:
            self.progress.update(task_id, **kwargs)
