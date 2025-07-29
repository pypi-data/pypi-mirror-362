from doteval.evaluators import exact_match, numeric_match, valid_json
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


def test_exact_match_default_name():
    """Test that exact_match uses default name when no custom name provided"""
    score = exact_match("1", "1")
    assert score.name == "exact_match"


def test_exact_match_custom_name():
    """Test that exact_match uses custom name when provided"""
    score = exact_match("1", "1", name="custom_comparison")
    assert score.name == "custom_comparison"
    assert score.value is True


def test_exact_match_custom_name_with_failure():
    """Test that custom name works with failed evaluations"""
    score = exact_match("1", "2", name="my_custom_evaluator")
    assert score.name == "my_custom_evaluator"
    assert score.value is False


def test_exact_match_name_none():
    """Test that passing name=None falls back to default name"""
    score = exact_match("1", "1", name=None)
    assert score.name == "exact_match"


def test_numeric_match_custom_name():
    """Test that numeric_match supports custom names"""
    score = numeric_match("1234", "1,234", name="number_comparison")
    assert score.name == "number_comparison"
    assert score.value is True


def test_valid_json_custom_name():
    """Test that valid_json supports custom names"""
    score = valid_json('{"key": "value"}', name="json_validator")
    assert score.name == "json_validator"
    assert score.value is True
