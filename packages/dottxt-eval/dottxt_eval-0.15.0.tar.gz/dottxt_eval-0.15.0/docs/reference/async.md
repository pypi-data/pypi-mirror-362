# Async Evaluations

doteval provides robust support for asynchronous evaluations, enabling concurrent processing to significantly speed up large-scale LLM evaluations.

## Overview

Async evaluations allow you to:

- Run multiple evaluations concurrently
- Control concurrency levels to manage resource usage
- Leverage async/await patterns with async models
- Scale evaluations efficiently across large datasets

## Basic Async Evaluation

Define async evaluation functions using standard Python `async`/`await` syntax:

```python
import asyncio
import doteval
from doteval.evaluators import exact_match

dataset = [("What is 2+2?", "4"), ("What is 3+3?", "6")]

@doteval.foreach("question,answer", dataset)
async def eval_async_math(question, answer):
    # Simulate async model call
    await asyncio.sleep(0.1)
    result = await async_model.generate(question)
    return exact_match(result, answer)
```

## Concurrency Control

### Using Command Line Options

Control concurrency via command-line flags:

```bash
pytest eval_async.py --max-concurrency 20
```

### Using Custom Concurrency Strategies

For more fine-grained control, use custom concurrency strategies:

```python
from doteval import ForEach
from doteval.concurrency import SlidingWindowStrategy

# Configure sliding window concurrency
sliding_window = SlidingWindowStrategy(max_concurrency=20)
foreach = ForEach(concurrency=sliding_window)

@foreach("question,answer", dataset)
async def eval_with_strategy(question, answer):
    result = await async_model.generate(question)
    return exact_match(result, answer)
```

### Default Behavior

By default, async functions use the `SlidingWindowStrategy` with `max_concurrency=10`. This maintains up to 10 concurrent evaluations in a sliding window pattern:

- As each evaluation completes, a new one starts
- Maintains consistent resource usage
- Optimizes throughput for I/O-bound operations

## Running Async Evaluations

### With pytest

```bash
# Async evaluations work seamlessly with pytest
pytest eval_async.py --samples 1000
```

### Programmatically

```python
import asyncio

async def main():
    result = await eval_async_math(max_concurrency=10)
    print(f"Accuracy: {result.summary['exact_match']['accuracy']}")

asyncio.run(main())
```

## Async Models Integration

doteval works with various async model libraries:

### OpenAI Async Client

```python
import openai
import doteval
from doteval.evaluators import exact_match

client = openai.AsyncOpenAI()

@doteval.foreach("question,answer", dataset)
async def eval_openai_async(question, answer):
    response = await client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": question}]
    )
    result = response.choices[0].message.content
    return exact_match(result, answer)
```

### Anthropic Async Client

```python
import anthropic
import doteval

client = anthropic.AsyncAnthropic()

@doteval.foreach("question,answer", dataset)
async def eval_anthropic_async(question, answer):
    response = await client.messages.create(
        model="claude-3-sonnet-20240229",
        messages=[{"role": "user", "content": question}]
    )
    result = response.content[0].text
    return exact_match(result, answer)
```

### Custom Async Model

```python
class AsyncModel:
    async def generate(self, prompt: str) -> str:
        # Your async model implementation
        await asyncio.sleep(0.1)  # Simulate API call
        return "model response"

model = AsyncModel()

@doteval.foreach("question,answer", dataset)
async def eval_custom_async(question, answer):
    result = await model.generate(question)
    return exact_match(result, answer)
```

## Concurrency Patterns

### Sliding Window Concurrency

doteval uses a sliding window approach for optimal resource utilization:

```python
# Internal implementation (for reference)
async def _run_evaluation_async(eval_fn, dataset, max_concurrency):
    pending_tasks = set()

    # Fill initial window
    for _ in range(max_concurrency):
        if dataset_item := next(dataset, None):
            task = asyncio.create_task(eval_fn(*dataset_item))
            pending_tasks.add(task)

    # Process completed tasks and start new ones
    while pending_tasks:
        done, pending_tasks = await asyncio.wait(
            pending_tasks, return_when=asyncio.FIRST_COMPLETED
        )

        for task in done:
            result = await task
            # Process result...

            # Start new task if dataset has more items
            if dataset_item := next(dataset, None):
                new_task = asyncio.create_task(eval_fn(*dataset_item))
                pending_tasks.add(new_task)
```

### Rate Limiting

Implement rate limiting with a custom concurrency strategy:

```python
from doteval.concurrency import AsyncConcurrencyStrategy
from doteval import ForEach
import asyncio
from typing import AsyncIterator, Callable, TypeVar

T = TypeVar('T')

class RateLimitedStrategy:
    """Concurrency strategy with built-in rate limiting."""

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
            # Enforce rate limit
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

# Use the rate-limited strategy
rate_limited = RateLimitedStrategy(max_concurrency=10, requests_per_second=5)
foreach = ForEach(concurrency=rate_limited)

@foreach("question,answer", dataset)
async def eval_rate_limited(question, answer):
    result = await api_call(question)
    return exact_match(result, answer)
```

## Retry Configuration

### Default Retry Behavior

By default, async evaluations automatically retry on connection errors:

- **Retry count**: 3 attempts
- **Retry delay**: Exponential backoff with jitter (1s initial delay)
- **Retried errors**: Connection errors, timeouts, and network-related OS errors

### Custom Retry Strategy

Configure custom retry behavior using tenacity:

```python
from tenacity import AsyncRetrying, stop_after_attempt, wait_fixed, retry_if_exception_type
from doteval import ForEach
import aiohttp

# Custom retry for specific API errors
api_retries = AsyncRetrying(
    retry=retry_if_exception_type((aiohttp.ClientError, TimeoutError)),
    stop=stop_after_attempt(5),
    wait=wait_fixed(2)  # Fixed 2-second delay between retries
)

foreach = ForEach(retries=api_retries)

@foreach("question,answer", dataset)
async def eval_with_custom_retry(question, answer):
    # Will retry up to 5 times on aiohttp.ClientError or TimeoutError
    result = await api_client.generate(question)
    return exact_match(result, answer)
```

### Advanced Retry Configuration

```python
from tenacity import AsyncRetrying, stop_after_attempt, wait_exponential, retry_if_result

# Retry on specific conditions
def should_retry(result):
    """Retry if the API returns a rate limit response."""
    return hasattr(result, 'status_code') and result.status_code == 429

custom_retries = AsyncRetrying(
    retry=(retry_if_exception_type(Exception) | retry_if_result(should_retry)),
    stop=stop_after_attempt(10),
    wait=wait_exponential(multiplier=1, min=4, max=60)
)

foreach = ForEach(retries=custom_retries)
```

## Error Handling

Async evaluations provide robust error handling:

```python
@doteval.foreach("question,answer", dataset)
async def eval_with_error_handling(question, answer):
    try:
        result = await unreliable_api_call(question)
        return exact_match(result, answer)
    except Exception as e:
        # Error is captured in evaluation results
        raise e  # Re-raise to be handled by doteval
```

## Performance Optimization

### Batch Processing

Process multiple items in batches:

```python
@doteval.foreach("questions,answers", batched_dataset)
async def eval_batch(questions, answers):
    # Process batch of questions together
    results = await model.generate_batch(questions)
    scores = [exact_match(result, answer)
              for result, answer in zip(results, answers)]
    return scores
```

### Connection Pooling

Use connection pooling for HTTP-based APIs:

```python
import aiohttp

async def create_session():
    connector = aiohttp.TCPConnector(limit=100)
    return aiohttp.ClientSession(connector=connector)

session = await create_session()

@doteval.foreach("question,answer", dataset)
async def eval_with_session(question, answer):
    async with session.post("https://api.example.com", json={"prompt": question}) as resp:
        result = await resp.json()
        return exact_match(result["text"], answer)
```

## Monitoring and Progress

### Progress Tracking

```python
from tqdm.asyncio import tqdm

@doteval.foreach("question,answer", dataset)
async def eval_with_progress(question, answer):
    result = await model.generate(question)
    # Progress automatically tracked by doteval
    return exact_match(result, answer)
```

### Resource Monitoring

```python
import psutil
import asyncio

async def monitor_resources():
    while True:
        cpu_percent = psutil.cpu_percent()
        memory_percent = psutil.virtual_memory().percent
        print(f"CPU: {cpu_percent}%, Memory: {memory_percent}%")
        await asyncio.sleep(10)

# Run monitoring alongside evaluations
async def main():
    monitor_task = asyncio.create_task(monitor_resources())
    eval_task = asyncio.create_task(eval_async_math())

    result = await eval_task
    monitor_task.cancel()
    return result
```

## Best Practices

### Concurrency Levels

- **CPU-bound tasks**: `max_concurrency = number_of_cores`
- **I/O-bound tasks**: `max_concurrency = 10-100` (depending on API limits)
- **Memory-intensive tasks**: Lower concurrency to avoid OOM

### API Rate Limits

```python
# Respect API rate limits
@doteval.foreach("question,answer", dataset)
async def eval_api_limited(question, answer):
    # Add delays for rate limiting
    await asyncio.sleep(0.1)  # 10 requests per second
    result = await api_call(question)
    return exact_match(result, answer)
```

### Resource Cleanup

```python
class AsyncModel:
    async def __aenter__(self):
        self.client = await create_client()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.close()

async with AsyncModel() as model:
    @doteval.foreach("question,answer", dataset)
    async def eval_with_cleanup(question, answer):
        result = await model.generate(question)
        return exact_match(result, answer)

    result = await eval_with_cleanup()
```

### Memory Management

```python
# For large datasets, use generators to avoid loading everything into memory
def stream_dataset():
    for i in range(1000000):
        yield (f"Question {i}", f"Answer {i}")

@doteval.foreach("question,answer", stream_dataset())
async def eval_streaming(question, answer):
    result = await model.generate(question)
    return exact_match(result, answer)
```

## Debugging Async Issues

### Common Pitfalls

1. **Blocking calls in async functions**:
```python
# ❌ Wrong - blocks the event loop
@doteval.foreach("question,answer", dataset)
async def eval_blocking(question, answer):
    result = synchronous_model.generate(question)  # Blocks!
    return exact_match(result, answer)

# ✅ Correct - use thread pool for blocking calls
import asyncio
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor(max_workers=4)

@doteval.foreach("question,answer", dataset)
async def eval_non_blocking(question, answer):
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(
        executor, synchronous_model.generate, question
    )
    return exact_match(result, answer)
```

2. **Not awaiting async calls**:
```python
# ❌ Wrong - returns coroutine object
@doteval.foreach("question,answer", dataset)
async def eval_not_awaited(question, answer):
    result = model.generate(question)  # Missing await!
    return exact_match(result, answer)

# ✅ Correct
@doteval.foreach("question,answer", dataset)
async def eval_awaited(question, answer):
    result = await model.generate(question)
    return exact_match(result, answer)
```

### Performance Profiling

```python
import time

@doteval.foreach("question,answer", dataset)
async def eval_with_timing(question, answer):
    start_time = time.time()
    result = await model.generate(question)
    duration = time.time() - start_time

    score = exact_match(result, answer)
    score.metadata["duration"] = duration
    return score
```
