# doteval

LLM evaluation library that works like pytest.

## Overview

doteval lets you write LLM evaluations as pytest test functions. It handles progress tracking, resumption after crashes, and result storage automatically.

```python
from doteval import foreach, Result
from doteval.evaluators import exact_match

@foreach("question,answer", dataset)
def eval_math_questions(question, answer, model):
    response = model.generate(question)
    return Result(prompt=question, scores=[exact_match(response, answer)])
```

`pytest` will collect all `eval_` functions in `eval_*.py` files and run them as an evaluation:

```bash
pytest eval_math_questions.py --experiment my_evaluation
```

## Installation

```bash
pip install dottxt-eval
```

## Basic Usage

### 1. Write an evaluation function

```python
# eval_sentiment.py
import pytest
from doteval import foreach, Result
from doteval.evaluators import exact_match

@pytest.fixture
def model():
    return load_your_model()

data = [
    ("I love this!", "positive"),
    ("This is terrible", "negative"),
    ("It's okay", "neutral")
]

@foreach("text,label", data)
def eval_sentiment(text, label, model):
    prediction = model.classify(text)
    return Result(prompt=text, scores=[exact_match(prediction, label)])
```

### 2. Run the evaluation

```bash
pytest eval_sentiment.py --experiment sentiment_test
```

### 3. View results

```bash
doteval show sentiment_test
```

## Key Features

- **Automatic resumption**: Crashed evaluations continue where they left off
- **Session management**: Named experiments with persistent storage
- **pytest integration**: Use all pytest features (fixtures, parametrization, etc.)
- **Async support**: Built-in concurrency control for large-scale evaluations

## Examples

### Math Reasoning

```python
from datasets import load_dataset
from doteval import foreach, Result
from doteval.evaluators import exact_match

def gsm8k_dataset():
    dataset = load_dataset("gsm8k", "main", split="test", streaming=True)
    for item in dataset:
        yield (item["question"], extract_answer(item["answer"]))

@foreach("question,answer", gsm8k_dataset())
def eval_math_reasoning(question, answer, model):
    response = model.solve(question)
    return Result(prompt=question, scores=[exact_match(extract_number(response), answer)])
```

### Async Evaluation

```python
@foreach("text,label", large_dataset)
async def eval_classification(text, label, async_model):
    prediction = await async_model.classify(text)
    return Result(prompt=text, scores=[exact_match(prediction, label)])
```

```bash
pytest eval_classification.py --experiment async_eval
```

### Custom Evaluators

```python
from doteval.evaluators import evaluator
from doteval.metrics import accuracy

@evaluator(metrics=accuracy())
def semantic_similarity(response: str, expected: str) -> bool:
    embedding1 = get_embedding(response)
    embedding2 = get_embedding(expected)
    return cosine_similarity(embedding1, embedding2) > 0.8

@foreach("question,answer", dataset)
def eval_qa(question, answer, model):
    response = model.generate(question)
    return Result(prompt=question, scores=[semantic_similarity(response, answer)])
```

## CLI Commands

```bash
# List all evaluation experiments
doteval list

# Show results for a specific experiment
doteval show experiment_name

# Show results with error details
doteval show experiment_name --errors

# Show full results without truncation
doteval show experiment_name --full

# Delete an experiment
doteval delete experiment_name

# Rename an experiment
doteval rename old_name new_name

# Use custom storage backend for any command
doteval list --storage sqlite://results.db
doteval show experiment_name --storage sqlite://results.db
doteval delete experiment_name --storage sqlite://results.db
doteval rename old_name new_name --storage sqlite://results.db

# Run with limited samples for testing
pytest eval_test.py --experiment eval_run --samples 10
```

## Session Management

Experiments automatically track:
- Evaluation progress and completion status
- Individual sample results and errors
- Timing and performance metrics
- Resumption state for interrupted runs

```bash
# Start named experiment
pytest eval_math.py --experiment math_baseline

# Resume if interrupted
pytest eval_math.py --experiment math_baseline  # Continues from last completed sample

# Use different storage backend
pytest eval_math.py --experiment math_baseline --storage sqlite://results.db
```

## Custom Retry and Concurrency Strategies

doteval allows you to customize retry logic and concurrency strategies for your evaluations:

### Retry Configuration

Use tenacity's `AsyncRetrying` to customize retry behavior:

```python
from tenacity import AsyncRetrying, stop_after_attempt, wait_exponential
from doteval import ForEach

# Custom retry strategy with exponential backoff
custom_retries = AsyncRetrying(
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=1, min=4, max=60)
)

# Apply to all evaluations in this instance
foreach = ForEach(retries=custom_retries)

@foreach("question,answer", dataset)
async def eval_with_retries(question, answer, model):
    response = await model.generate(question)  # Will retry up to 5 times
    return Result(prompt=question, scores=[exact_match(response, answer)])
```

### Concurrency Strategies

Control how evaluations are executed with custom concurrency strategies:

```python
from doteval import ForEach
from doteval.concurrency import SlidingWindowStrategy, BatchStrategy, AdaptiveStrategy

# For async functions - sliding window concurrency
sliding_window = SlidingWindowStrategy(max_concurrency=20)
foreach = ForEach(concurrency=sliding_window)

@foreach("text,label", large_dataset)
async def eval_async(text, label, model):
    response = await model.classify(text)
    return Result(prompt=text, scores=[exact_match(response, label)])

# For sync functions - batch processing
batch_strategy = BatchStrategy(batch_size=50)
foreach_batch = ForEach(concurrency=batch_strategy)

@foreach_batch("text,label", dataset)
def eval_in_batches(text, label, model):
    response = model.classify(text)
    return Result(prompt=text, scores=[exact_match(response, label)])

# For async functions - adaptive concurrency that automatically adjusts
adaptive_strategy = AdaptiveStrategy(
    initial_concurrency=5,
    min_concurrency=1,
    max_concurrency=50,
    adaptation_interval=2.0
)
foreach_adaptive = ForEach(concurrency=adaptive_strategy)

@foreach_adaptive("text,label", large_dataset)
async def eval_adaptive(text, label, model):
    response = await model.classify(text)
    return Result(prompt=text, scores=[exact_match(response, label)])
```

### Adaptive Concurrency Strategy

The `AdaptiveStrategy` automatically adjusts concurrency levels based on throughput to maximize performance:

```python
from doteval.concurrency import AdaptiveStrategy

# Create an adaptive strategy
adaptive = AdaptiveStrategy(
    initial_concurrency=5,      # Starting concurrency level
    min_concurrency=1,          # Minimum concurrency limit
    max_concurrency=100,        # Maximum concurrency limit
    adaptation_interval=2.0,    # Seconds between adaptation decisions
    increase_threshold=0.98,    # Increase if throughput ratio > this
    decrease_threshold=0.90,    # Decrease if throughput ratio < this
    stability_window=3,         # Number of measurements before changing direction
    error_backoff_factor=0.7    # Multiply concurrency by this on errors
)

foreach = ForEach(concurrency=adaptive)

@foreach("prompt,expected", large_dataset)
async def eval_with_adaptive_concurrency(prompt, expected, model):
    response = await model.generate(prompt)
    return Result(prompt=prompt, scores=[exact_match(response, expected)])

# Get adaptation statistics
stats = adaptive.get_stats()
print(f"Current concurrency: {stats['current_concurrency']}")
print(f"Throughput: {stats['throughput']:.2f} requests/second")
print(f"Total completed: {stats['total_completed']}")
```

**Key Features:**
- **Progressive Increase**: Starts conservatively and increases based on observed throughput
- **Hill-Climbing**: Continuously finds the optimal concurrency level
- **Error Backoff**: Automatically reduces concurrency when errors occur
- **Stability Windows**: Prevents oscillation by waiting for consistent improvements
- **Throughput Tracking**: Measures requests per second in a sliding window

This strategy is ideal for saturating remote GPU resources where you don't have explicit usage information.

### Custom Concurrency Strategy

Implement your own concurrency strategy:

```python
import asyncio
from typing import AsyncIterator, Callable, TypeVar

T = TypeVar('T')

class RateLimitedStrategy:
    def __init__(self, max_concurrency: int, requests_per_second: float):
        self.max_concurrency = max_concurrency
        self.requests_per_second = requests_per_second
        self.min_interval = 1.0 / requests_per_second

    async def execute(
        self,
        tasks: AsyncIterator[Callable[[], T]],
        progress_callback: Callable[[T], None] | None = None
    ) -> AsyncIterator[T]:
        last_request_time = 0
        pending = set()

        async for task in tasks:
            # Rate limiting
            current_time = asyncio.get_event_loop().time()
            time_since_last = current_time - last_request_time
            if time_since_last < self.min_interval:
                await asyncio.sleep(self.min_interval - time_since_last)

            # Manage concurrency
            if len(pending) >= self.max_concurrency:
                done, pending = await asyncio.wait(
                    pending, return_when=asyncio.FIRST_COMPLETED
                )
                for completed in done:
                    result = await completed
                    if progress_callback:
                        progress_callback(result)
                    yield result

            pending.add(asyncio.create_task(task()))
            last_request_time = asyncio.get_event_loop().time()

        # Process remaining tasks
        while pending:
            done, pending = await asyncio.wait(
                pending, return_when=asyncio.FIRST_COMPLETED
            )
            for completed in done:
                result = await completed
                if progress_callback:
                    progress_callback(result)
                yield result

# Use the custom strategy
rate_limited = RateLimitedStrategy(max_concurrency=10, requests_per_second=5)
foreach = ForEach(concurrency=rate_limited)
```

### Complete Example

```python
from tenacity import AsyncRetrying, stop_after_attempt, wait_fixed, retry_if_exception_type
from doteval import ForEach, Result
from doteval.concurrency import SlidingWindowStrategy
from doteval.evaluators import exact_match
import aiohttp

# Configure retry for specific exceptions
api_retries = AsyncRetrying(
    retry=retry_if_exception_type((aiohttp.ClientError, TimeoutError)),
    stop=stop_after_attempt(3),
    wait=wait_fixed(2)
)

# Configure concurrency
concurrency = SlidingWindowStrategy(max_concurrency=5)

# Create configured ForEach instance
foreach = ForEach(retries=api_retries, concurrency=concurrency)

@foreach("prompt,expected", test_prompts)
async def eval_api_responses(prompt, expected, api_client):
    # This will retry on API errors and run up to 5 concurrent requests
    response = await api_client.complete(prompt)
    return Result(prompt=response, scores=[exact_match(response, expected)])
```

## Storage Backends

doteval supports multiple storage backends and allows you to implement custom ones:

```python
# Built-in backends
from doteval.sessions import SessionManager

# JSON storage (default)
manager = SessionManager(storage_path="json://.doteval")

# SQLite storage with query capabilities
manager = SessionManager(storage_path="sqlite://evaluations.db")

# Custom backend
from doteval.storage import Storage, register

class MyStorage(Storage):
    # Implement abstract methods...
    pass

register("mybackend", MyStorage)
manager = SessionManager(storage_path="mybackend://config")
```
