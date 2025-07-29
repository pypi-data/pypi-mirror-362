import time
from collections import defaultdict
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional

from doteval.metrics import Metric


class EvaluationStatus(Enum):
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class Evaluation:
    evaluation_name: str
    status: EvaluationStatus
    started_at: float
    metadata: dict[str, str] = field(default_factory=dict)
    completed_at: Optional[float] = None


@dataclass
class Result:
    prompt: Optional[str]
    scores: list["Score"]
    error: Optional[str] = None
    model_response: Optional[str] = None

    def __init__(
        self,
        *scores: "Score",
        prompt: Optional[str] = None,
        error: Optional[str] = None,
        model_response: Optional[str] = None,
    ):
        self.prompt = prompt
        self.scores = list(scores)
        self.error = error
        self.model_response = model_response


@dataclass
class Score:
    name: str
    value: Any
    metrics: list[Metric]
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class Record:
    """Record of evaluating a single dataset item"""

    result: Result
    item_id: int
    dataset_row: dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None
    timestamp: float = field(default_factory=time.time)


class EvaluationSummary:
    """Aggregated results of a full evaluation"""

    def __init__(self, results: list[Record]):
        self.results = results
        self.summary = self.compute_summary()

    def compute_summary(self):
        summary = defaultdict(dict)

        # First pass: determine the expected score structure from successful results
        expected_scores = []
        for result in self.results:
            if result.error is None and result.result.scores:
                expected_scores = [
                    (score.name, score.metrics) for score in result.result.scores
                ]
                break

        # Regorganize the results by evaluator and metric
        aggregated_results = defaultdict(lambda: defaultdict(list))
        for result in self.results:
            if result.error is not None:
                # For error cases, add False values for each expected score
                for score_name, metrics in expected_scores:
                    for metric in metrics:
                        aggregated_results[score_name][metric].append(False)
            else:
                # For successful cases, use actual scores
                for score in result.result.scores:
                    for metric in score.metrics:
                        aggregated_results[score.name][metric].append(score.value)

        for evaluator_name, metrics_values in aggregated_results.items():
            for metrics, values in metrics_values.items():
                summary[evaluator_name][metrics.__name__] = metrics(values)

        return summary
