# Welcome to doteval!

**doteval** is a powerful evaluation framework for Large Language Models that makes testing and measuring LLM performance simple, reproducible, and scalable. Built by [dottxt](https://dottxt.co), it provides a clean, code-first approach to LLM evaluation.

## Core Concepts

### Evaluations with `@foreach`

The heart of doteval is the `@foreach` decorator that transforms a regular function into an evaluation that runs across an entire dataset:

```python
from doteval import foreach
from doteval.evaluators import exact_match

@foreach("question,answer", math_dataset)
def eval_math_reasoning(question, answer, model):
    """Evaluate mathematical reasoning ability."""
    result = model.solve(question)
    return exact_match(result, answer)
```

This simple decorator handles:

- **Data iteration** - Automatically processes each item in your dataset
- **Error handling** - Gracefully handles failures and continues evaluation
- **Progress tracking** - Shows real-time progress and estimates
- **Session management** - Saves state to resume interrupted evaluations

### Evaluators: Scoring Model Performance

Evaluators define how to score model outputs. doteval includes common evaluators and makes it easy to create custom ones:

```python
from doteval.evaluators import evaluator, exact_match
from doteval.metrics import accuracy

# Built-in evaluator
score = exact_match("42", "42")  # True

# Custom evaluator
@evaluator(metrics=accuracy())
def contains_reasoning(response: str) -> bool:
    """Check if response includes reasoning keywords."""
    keywords = ["because", "therefore", "since", "thus"]
    return any(keyword in response.lower() for keyword in keywords)
```

### Session Management

doteval automatically manages evaluation sessions, allowing you to:

- **Resume interrupted evaluations** - Power outages, crashes, or manual stops don't lose progress
- **Track multiple experiments** - Organize evaluations by name and compare results
- **Monitor real-time progress** - See completion rates and estimated time remaining

```bash
# Run evaluation
pytest eval_gsm8k.py --session my_experiment

# View results
doteval show my_experiment

# Resume if interrupted
pytest eval_gsm8k.py --session my_experiment  # Automatically resumes
```

### Flexible Data Handling

doteval works with any data format:

```python
# Hugging Face datasets
from datasets import load_dataset
dataset = load_dataset("gsm8k", "main", split="test")

# Custom generators
def my_dataset():
    for item in load_my_data():
        yield (item.question, item.answer)

# Simple lists
dataset = [
    ("What is 2+2?", "4"),
    ("What is 3+3?", "6"),
]

@foreach("question,answer", dataset)
def eval_arithmetic(question, answer, model):
    # Evaluation logic here
    pass
```

## Integration with pytest

doteval integrates seamlessly with pytest, giving you access to the entire pytest ecosystem:

```python
import pytest
from doteval import foreach

@pytest.fixture
def model():
    """Load your model once for all tests."""
    return load_my_model()

@foreach("prompt,expected", test_dataset)
def test_generation_quality(prompt, expected, model):
    """Test that generation meets quality standards."""
    response = model.generate(prompt)
    return quality_score(response, expected)

@foreach("question,answer", math_dataset)
def test_math_accuracy(question, answer, model):
    """Test mathematical reasoning accuracy."""
    result = model.solve(question)
    return exact_match(result, answer)
```

Run with standard pytest commands:

```bash
# Run all evaluations
pytest tests/

# Run specific evaluation with session
pytest eval_math.py::test_math_accuracy --session math_baseline

# Limit samples for quick testing
pytest eval_large.py --session quick_test --samples 100
```

## Async and Concurrency

Scale your evaluations with built-in async support:

```python
import asyncio
from doteval import foreach

@foreach("prompt,expected", large_dataset)
async def eval_async_model(prompt, expected, async_model):
    """Async evaluation for better throughput."""
    response = await async_model.generate_async(prompt)
    return exact_match(response, expected)
```

Control concurrency to balance speed and resource usage:

```bash
pytest eval_async.py --session large_eval --max-concurrency 50
```

## Rich CLI Experience

Manage your evaluations with a beautiful command-line interface:

```bash
# List all evaluation sessions
doteval list

# Filter by status or name
doteval list --status "Running" --name "gsm8k"

# View detailed results
doteval show my_experiment

# Full session data in JSON
doteval show my_experiment --full

# Clean up old experiments
doteval delete old_experiment
```

## Example: Complete Evaluation Pipeline

Here's a complete example evaluating a model on mathematical reasoning:

```python title="eval_math.py"
import pytest
from datasets import load_dataset
from doteval import foreach
from doteval.evaluators import exact_match
import re

@pytest.fixture
def model():
    """Load your model."""
    from your_model_library import load_model
    return load_model("your-math-model")

def extract_answer(response: str) -> str:
    """Extract numerical answer from response."""
    match = re.search(r'(\d+(?:\.\d+)?)', response)
    return match.group(1) if match else ""

def math_dataset():
    """Load and format GSM8K dataset."""
    dataset = load_dataset("gsm8k", "main", split="test", streaming=True)
    for item in dataset:
        question = item["question"]
        # Extract answer from solution
        answer_match = re.search(r'#### (\d+)', item["answer"])
        answer = answer_match.group(1) if answer_match else ""
        yield (question, answer)

@foreach("question,answer", math_dataset())
def eval_math_reasoning(question, answer, model):
    """Evaluate mathematical reasoning on GSM8K."""
    prompt = f"Solve this step by step:\n\n{question}\n\nAnswer:"
    response = model.generate(prompt, max_tokens=200)
    predicted_answer = extract_answer(response)
    return exact_match(predicted_answer, answer)
```

Run the evaluation:

```bash
# Start evaluation
pytest eval_math.py::eval_math_reasoning --session gsm8k_baseline

# Monitor progress
doteval list

# View results when complete
doteval show gsm8k_baseline
```

## Next Steps

Ready to get started? Here's what to do next:

1. **[Install doteval](installation.md)** - Get up and running in minutes
2. **[Try the quickstart](quickstart.md)** - Build your first evaluation
3. **[Explore examples](../cookbook/index.md)** - See real-world evaluation setups
4. **[Read the reference](../reference/index.md)** - Deep dive into all features

## Why Choose doteval?

doteval is built by the team at [dottxt](https://dottxt.co) with decades of experience in machine learning, software engineering, and language model evaluation. We're a VC-backed company fully focused on structured generation and evaluation, committed to making the community benefit from our expertise.

**Key advantages:**

- **Battle-tested** - Used in production for large-scale LLM evaluations
- **Community-driven** - Open source with active development and support
- **Extensible** - Designed to grow with your evaluation needs
- **Reliable** - Robust error handling and session management
- **Fast** - Optimized for performance with async and concurrency support

Join the community and start evaluating your models with confidence!
