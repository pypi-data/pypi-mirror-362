"""Integration tests for fixture handling with foreach decorator."""

import pytest

from doteval import foreach
from doteval.evaluators import exact_match
from doteval.models import Result


# Test fixture that will be used with indirect parametrization
@pytest.fixture
def application(request):
    """Fixture that processes application configuration from parametrized values."""
    model_name = request.param

    # Simulate different model configurations
    if model_name == "model_a":
        model = lambda prompt: "result_a"
        template = lambda **kwargs: f"Model A: {kwargs.get('question', '')}"
        output_structure = {"type": "model_a"}
    elif model_name == "model_b":
        model = lambda prompt: "result_b"
        template = lambda **kwargs: f"Model B: {kwargs.get('question', '')}"
        output_structure = {"type": "model_b"}
    else:
        model = lambda prompt: "result_c"
        template = lambda **kwargs: f"Model C: {kwargs.get('question', '')}"
        output_structure = {"type": "model_c"}

    return model, template, output_structure


# Test with foreach decorator directly on the test function
@pytest.mark.parametrize(
    "application",
    ["model_a", "model_b", "model_c"],
    indirect=True,
)
@foreach("question,answer", [("What is 2+2?", "4"), ("What is 3+3?", "6")])
def test_foreach_with_indirect_parametrization(question, answer, application):
    """Test that foreach decorator works with indirect parametrization."""
    model, template, output_structure = application
    prompt = template(question=question)

    # Simulate model processing
    result = model(prompt)

    # For testing, just check if we got a result
    score = (
        exact_match(result, "result_a")
        if output_structure["type"] == "model_a"
        else exact_match(result, result)
    )

    return Result(score, prompt=prompt)


# Test async version
@pytest.mark.parametrize(
    "application",
    ["model_a", "model_b"],
    indirect=True,
)
@foreach("question,answer", [("Async question?", "Async answer")])
async def test_async_foreach_with_indirect_parametrization(
    question, answer, application
):
    """Test that async foreach decorator works with indirect parametrization."""
    model, template, output_structure = application
    prompt = template(question=question)

    # Simulate async model processing
    import asyncio

    await asyncio.sleep(0.01)
    result = model(prompt)

    # For testing, just check if we got a result
    score = (
        exact_match(result, "result_a")
        if output_structure["type"] == "model_a"
        else exact_match(result, result)
    )

    return Result(score, prompt=prompt)


# Test with multiple fixtures
@pytest.fixture
def additional_config():
    """Another fixture to test multiple fixture resolution."""
    return {"extra": "config"}


@pytest.mark.parametrize(
    "application",
    ["model_a"],
    indirect=True,
)
@foreach("question,answer", [("Multi fixture test?", "42")])
def test_foreach_with_multiple_fixtures(
    question, answer, application, additional_config
):
    """Test that foreach works with multiple fixtures including indirect ones."""
    model, template, output_structure = application
    prompt = template(question=question)

    # Use both fixtures
    result = model(prompt)
    extra = additional_config.get("extra", "")

    score = (
        exact_match(result, "result_a")
        if output_structure["type"] == "model_a"
        else exact_match(result, result)
    )

    return Result(score, prompt=f"{prompt} [{extra}]")
