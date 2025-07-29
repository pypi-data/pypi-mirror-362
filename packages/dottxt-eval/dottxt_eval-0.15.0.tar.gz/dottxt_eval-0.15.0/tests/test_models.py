from doteval.metrics import accuracy
from doteval.models import EvaluationSummary, Record, Result, Score


def test_summary_empty_results():
    results = []
    summary = EvaluationSummary(results)
    assert isinstance(summary.summary, dict)
    assert len(summary.summary) == 0


def test_summary_simple():
    result1 = Result(Score("match", True, [accuracy()]), prompt="test1")
    result2 = Result(Score("match", True, [accuracy()]), prompt="test2")
    results = [
        Record(result1, 1),
        Record(result2, 2),
    ]
    summary = EvaluationSummary(results)
    assert isinstance(summary.summary, dict)
    assert summary.summary == {"match": {"accuracy": 1.0}}


def test_summary_two_scores_result():
    result1 = Result(
        Score("match_1", True, [accuracy()]),
        Score("match_2", False, [accuracy()]),
        prompt="test1",
    )
    result2 = Result(
        Score("match_1", True, [accuracy()]),
        Score("match_2", False, [accuracy()]),
        prompt="test2",
    )
    results = [
        Record(result1, 1),
        Record(result2, 2),
    ]
    summary = EvaluationSummary(results)
    assert isinstance(summary.summary, dict)
    assert summary.summary == {
        "match_1": {"accuracy": 1.0},
        "match_2": {"accuracy": 0.0},
    }
