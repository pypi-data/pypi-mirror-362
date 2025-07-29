import asyncio
import inspect

import pytest


@pytest.hookimpl
def pytest_addoption(parser):
    """Add command line options that are specific to doteval.

    This hook registers custom CLI options that doteval users can pass to pytest:
    - --samples: Limit the number of dataset samples to evaluate
    - --experiment: Name the experiment for result storage
    """
    parser.addoption(
        "--samples", type=int, help="Maximum number of dataset samples to evaluate"
    )
    parser.addoption("--experiment", type=str, help="Name of the experiment")


@pytest.hookimpl
def pytest_configure(config):
    """Configure pytest for doteval integration.

    This hook extends pytest's collection patterns to include doteval evaluation files:
    - Collects files named `eval_*.py` (in addition to `test_*.py`)
    - Collects functions named `eval_*` (in addition to `test_*`)
    - Registers the 'doteval' marker for filtering evaluations vs tests
    - Initializes storage for evaluation results
    """
    config.addinivalue_line("markers", "doteval: mark test as LLM evaluation")
    config.addinivalue_line("python_files", "eval_*.py")
    config.addinivalue_line("python_functions", "eval_*")
    config._evaluation_results = {}


@pytest.hookimpl
def pytest_pyfunc_call(pyfuncitem):
    """Intercept function calls for doteval functions.

    This hook prevents pytest from trying to call doteval functions directly.
    Instead, we handle the execution in pytest_runtest_call where we can:
    - Pass the proper evaluation parameters (evaluation_name, experiment_name, samples)
    - Handle fixture resolution correctly
    - Run the actual evaluation logic

    Returning True indicates to pytest that we handled the call.

    """
    if hasattr(pyfuncitem.function, "_column_names"):
        # For doteval functions, return True to indicate we handled the call
        # This prevents the RuntimeError from the wrapper
        return True


@pytest.hookimpl
def pytest_generate_tests(metafunc):
    """Prevent fixture resolution errors for doteval functions.

    The problem: When pytest sees a function like `def eval_func(input, expected)`,
    it thinks 'input' and 'expected' are fixtures that need to be resolved. Pytest
    fixture resolution happens before our plugin is called.

    The solution: We pre-parametrize dataset column names with dummy values [None]
    to satisfy pytest's fixture resolution.

    Later, in pytest_runtest_call, our wrapper function will filter out these
    dummy values and only pass real fixture values to the evaluation.

    """
    if hasattr(metafunc.function, "_column_names"):
        column_names = metafunc.function._column_names

        # Only parametrize dataset columns that pytest thinks are fixtures
        for column in column_names:
            if column in metafunc.fixturenames:
                metafunc.parametrize(column, [None])


@pytest.hookimpl(tryfirst=True)
def pytest_collection_modifyitems(config, items):
    """Mark doteval functions for filtering and progress display.

    This hook identifies doteval functions and marks them with the 'doteval' marker.
    This allows users to run only evaluations or only tests:

        >>> pytest -m "doteval"      # Run only evaluations
        >>> pytest -m "not doteval"  # Run only regular tests

    The tryfirst=True ensures this runs before other plugins that might modify items.
    """
    for item in items:
        if hasattr(item.function, "_column_names"):
            item.add_marker(pytest.mark.doteval)


@pytest.hookimpl
def pytest_runtest_call(item):
    """Execute the evaluation function with proper parameter handling.

    This is the core execution hook that runs doteval functions. It:
    1. Extracts the column_names and CLI options (samples, experiment_name)
    2. Inspects the original function signature to identify expected parameters
    3. Separates dataset columns from fixture parameters
    4. Calls the wrapped evaluation function with proper arguments
    5. Handles async results by running them with asyncio.run()
    6. Stores results in the pytest config for later retrieval

    The function receives evaluation_name, experiment_name, and samples as
    special parameters, while fixture values are filtered and passed as **kwargs.
    """
    if hasattr(item.function, "_column_names"):
        eval_fn = item.function
        column_names = item.function._column_names
        samples = item.config.getoption("--samples")
        experiment_name = item.config.getoption("--experiment")

        # Get the fixture values that the function actually expects
        # We need to get the original function to inspect its signature
        original_func = getattr(eval_fn, "__wrapped__", eval_fn)
        sig = inspect.signature(original_func)
        expected_params = set(sig.parameters.keys())

        columns = set(column_names)
        expected_fixture_params = expected_params - columns

        fixture_kwargs = {}
        if hasattr(item, "funcargs"):
            for param_name in expected_fixture_params:
                if param_name in item.funcargs:
                    fixture_kwargs[param_name] = item.funcargs[param_name]

        evaluation_name = item.name

        result = eval_fn(
            evaluation_name=evaluation_name,
            experiment_name=experiment_name,
            samples=samples,
            **fixture_kwargs,
        )

        # If it's a coroutine, run it with asyncio.run
        if asyncio.iscoroutine(result):
            result = asyncio.run(result)

        item.config._evaluation_results[evaluation_name] = result
