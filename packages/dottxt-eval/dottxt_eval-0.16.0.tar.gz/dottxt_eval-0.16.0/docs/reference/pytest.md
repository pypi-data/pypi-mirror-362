# Pytest Integration

doteval provides deep integration with pytest through a custom plugin that enables seamless LLM evaluation testing.

## Overview

The pytest plugin automatically:

- Collects evaluation files (`eval_*.py`) and functions (`eval_*`)
- Provides custom command-line options for evaluation control
- Manages evaluation sessions and storage
- Integrates with pytest fixtures and parametrization

## Installation

The pytest plugin is automatically installed when you install doteval:

```bash
uv add doteval
```

The plugin is registered in `pyproject.toml`:

```toml
[project.entry-points.pytest11]
doteval = "doteval.plugin"
```

## File and Function Collection

The plugin extends pytest's collection to include:

- **Files**: `eval_*.py` (in addition to standard `test_*.py`)
- **Functions**: `eval_*` (in addition to standard `test_*`)

```python
# This file will be collected by pytest
# eval_math.py

import doteval
from doteval.evaluators import exact_match

dataset = [("2+2", "4"), ("3+3", "6")]

@doteval.foreach("question,answer", dataset)
def eval_arithmetic(question, answer):
    # Your evaluation logic
    result = model.generate(question)
    return exact_match(result, answer)
```

## Command Line Options

The plugin adds several command-line options:

### `--samples`

Limit the number of samples from each dataset:

```bash
pytest eval_math.py --samples 100
```

### `--session`

Specify a session name for tracking and resumption:

```bash
pytest eval_math.py --session my_experiment
```

### `--storage`

Choose the storage backend:

```bash
pytest eval_math.py --storage json
pytest eval_math.py --storage memory
```

## Pytest Fixtures Integration

doteval evaluations work seamlessly with pytest fixtures:

```python
import pytest
import doteval
from doteval.evaluators import exact_match

@pytest.fixture
def model():
    """Initialize model once for all tests."""
    return YourModel()

@pytest.fixture
def template():
    """Create a prompt template."""
    return "Q: {question}\nA:"

dataset = [("What is 2+2?", "4"), ("What is 3+3?", "6")]

@doteval.foreach("question,answer", dataset)
def eval_math_with_fixtures(question, answer, model, template):
    prompt = template.format(question=question)
    result = model.generate(prompt)
    return exact_match(result, answer)
```

## Markers

All doteval evaluations are automatically marked with `@pytest.mark.doteval`:

```bash
# Run only doteval evaluations
pytest -m doteval

# Skip doteval evaluations
pytest -m "not doteval"
```

## Session Management

The plugin automatically manages evaluation sessions:

- **Session Start**: Initializes session storage before tests run
- **Progress Tracking**: Tracks completion status of each evaluation
- **Resumption**: Allows resuming interrupted evaluations

```bash
# Start a named session
pytest eval_large_dataset.py --session experiment_1

# Resume if interrupted
pytest eval_large_dataset.py --session experiment_1
```

## Execution Hooks

The plugin implements several pytest hooks:

### `pytest_configure`

Configures pytest to collect evaluation files and functions:

```python
@pytest.hookimpl
def pytest_configure(config):
    config.addinivalue_line("markers", "doteval: mark test as LLM evaluation")
    config.addinivalue_line("python_files", "eval_*.py")
    config.addinivalue_line("python_functions", "eval_*")
```

### `pytest_runtest_call`

Executes the actual evaluation:

```python
@pytest.hookimpl
def pytest_runtest_call(item):
    if hasattr(item.function, "_eval_fn"):
        # Execute doteval function
        return item.function()
    else:
        # Standard pytest execution
        return None
```

## Parametrized Tests

doteval works with pytest parametrization:

```python
import pytest
import doteval

@pytest.mark.parametrize("model_name", ["gpt-3.5", "gpt-4"])
@doteval.foreach("question,answer", dataset)
def eval_multiple_models(question, answer, model_name):
    model = load_model(model_name)
    result = model.generate(question)
    return exact_match(result, answer)
```

## Error Handling

The plugin provides robust error handling:

- Individual evaluation failures don't stop the entire test suite
- Errors are captured and stored in the evaluation results
- Detailed error reporting in test output

## Configuration

You can configure the plugin behavior in `pytest.ini`:

```ini
[tool:pytest]
# Collect only evaluation files
python_files = eval_*.py
python_functions = eval_*

# Set default markers
markers =
    doteval: LLM evaluation tests
    slow: tests that take a long time
```

## Best Practices

### File Organization

```
tests/
├── eval_math.py        # Math evaluations
├── eval_reasoning.py   # Reasoning evaluations
└── fixtures/
    ├── conftest.py     # Shared fixtures
    └── models.py       # Model fixtures
```

### Fixture Scope

Use appropriate fixture scopes for expensive resources:

```python
@pytest.fixture(scope="session")
def expensive_model():
    """Load model once per test session."""
    return load_large_model()

@pytest.fixture(scope="module")
def dataset():
    """Load dataset once per module."""
    return load_dataset()
```

### Session Naming

Use descriptive session names:

```bash
pytest eval_math.py --session "baseline_gpt35_v1"
pytest eval_math.py --session "improved_prompt_v2"
```
