from doteval.evaluators import exact_match
from doteval.models import Score


def test_match():
    score = exact_match("1", "1")
    assert isinstance(score, Score)
    assert isinstance(score.metrics, list)
    assert len(score.metrics) == 1
    assert score.metrics[0].__name__ == "accuracy"
    assert score.value is True

    score = exact_match("1", "2")
    assert score.value is False
