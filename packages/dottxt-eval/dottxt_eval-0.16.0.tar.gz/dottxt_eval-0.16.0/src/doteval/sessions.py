import time
import uuid
from datetime import datetime
from typing import Optional, Union

from doteval.models import Evaluation, EvaluationStatus, Record
from doteval.storage import Storage, get_storage


class EvaluationProgress:
    """Runtime progress tracking for an evaluation.

    Used for progress bars.

    """

    def __init__(self, evaluation_name: str):
        self.evaluation_name = evaluation_name
        self.completed_count = 0
        self.error_count = 0
        self.start_time = time.time()


class SessionManager:
    """Manages experiment lifecycle and storage"""

    def __init__(
        self,
        storage: Optional[Union[Storage, str]] = None,
        experiment_name: Optional[str] = None,
    ):
        # Handle storage parameter - can be Storage instance or path string
        if isinstance(storage, Storage):
            self.storage = storage
        else:
            self.storage = get_storage(storage)

        self.evaluation_progress: EvaluationProgress | None = None
        self.active_evaluations: set[str] = set()

        # If no experiment name provided, create ephemeral one with timestamp
        if experiment_name is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            short_uuid = str(uuid.uuid4())[:8]
            experiment_name = f"{timestamp}_{short_uuid}"

        self.current_experiment: str = experiment_name
        self.storage.create_experiment(experiment_name)

    def start_evaluation(self, evaluation_name: str):
        evaluation = self.storage.load_evaluation(
            self.current_experiment, evaluation_name
        )

        if evaluation:
            completed_items = self.storage.completed_items(
                self.current_experiment, evaluation_name
            )
            print(
                f"{evaluation_name}: Resuming from {len(completed_items)} completed samples"
            )
        else:
            git_commit = get_git_commit()
            metadata = {"git_commit": git_commit} if git_commit else {}
            evaluation = Evaluation(
                evaluation_name=evaluation_name,
                status=EvaluationStatus.RUNNING,
                started_at=time.time(),
                metadata=metadata,
            )
            self.storage.create_evaluation(self.current_experiment, evaluation)

        self.evaluation_progress = EvaluationProgress(evaluation_name)
        self.active_evaluations.add(evaluation_name)

    def add_results(self, evaluation_name: str, results: list[Record]):
        self.storage.add_results(self.current_experiment, evaluation_name, results)

        if self.evaluation_progress:
            for result in results:
                self.evaluation_progress.completed_count += 1
                if result.error is not None:
                    self.evaluation_progress.error_count += 1

    def get_results(self, evaluation_name: str) -> list[Record]:
        return self.storage.get_results(self.current_experiment, evaluation_name)

    def finish_evaluation(self, evaluation_name: str, success: bool = True):
        status = EvaluationStatus.COMPLETED if success else EvaluationStatus.FAILED
        self.storage.update_evaluation_status(
            self.current_experiment, evaluation_name, status
        )

    def finish_all(self, success: bool = True):
        """Finish all active evaluations"""
        for evaluation_name in self.active_evaluations:
            self.finish_evaluation(evaluation_name, success)


def get_git_commit() -> Optional[str]:
    """Get git commit if available"""
    try:
        import subprocess

        return (
            subprocess.check_output(
                ["git", "rev-parse", "HEAD"], stderr=subprocess.DEVNULL
            )
            .decode()
            .strip()[:8]
        )
    except subprocess.CalledProcessError:
        return None
