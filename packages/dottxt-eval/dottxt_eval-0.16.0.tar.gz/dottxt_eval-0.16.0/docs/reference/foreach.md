# The @foreach Decorator

The `@foreach` decorator is the heart of doteval. It transforms a regular Python function into an evaluation that automatically runs across an entire dataset, handling data iteration, error management, progress tracking, and session management.

## Basic Usage

```python
from doteval import foreach
from doteval.evaluators import exact_match

@foreach("question,answer", dataset)
def eval_model(question, answer, model):
    """Evaluate model on question-answer pairs."""
    response = model.generate(question)
    return exact_match(response, answer)
```

## Function Signature

The `@foreach` decorator can be used in two ways:

### 1. Direct Usage (Default)

```python
def foreach(column_spec: str, dataset: Iterator) -> Callable
```

**Parameters:**

- **column_spec** (`str`): Comma-separated list of column names that map to dataset fields
- **dataset** (`Iterator`): An iterator of tuples/lists representing dataset rows

**Returns:** A decorated function that can be used as a regular function or pytest test

### 2. Configured Instance

```python
from doteval import ForEach

foreach = ForEach(
    dataset: Optional[Iterator] = None,
    name: Optional[str] = None,
    retries: Optional[AsyncRetrying] = None,
    concurrency: Optional[Union[AsyncConcurrencyStrategy, SyncConcurrencyStrategy]] = None,
    storage: Optional[Storage] = None
)
```

**Parameters:**

- **dataset** (`Optional[Iterator]`): Default dataset for all decorations
- **name** (`Optional[str]`): Name for the evaluation
- **retries** (`Optional[AsyncRetrying]`): Custom retry strategy using tenacity
- **concurrency** (`Optional[Union[AsyncConcurrencyStrategy, SyncConcurrencyStrategy]]`): Custom concurrency strategy
- **storage** (`Optional[Storage]`): Custom storage backend

**Returns:** A configured ForEach instance with custom behavior

## Registered Dataset Syntax

For built-in datasets, you can use the simplified `@foreach.dataset_name()` syntax:

```python
from doteval import foreach

@foreach.gsm8k("test")
def eval_math_reasoning(question, answer, model):
    """Evaluate on GSM8K dataset."""
    response = model.solve(question)
    return exact_match(response, answer)
```

This is equivalent to manually loading the dataset but provides:
- Automatic dataset loading and preprocessing
- Progress bars with dataset names and sizes
- Consistent column naming across datasets

### Available Registered Datasets

Currently available datasets:
- `gsm8k`: Grade school math problems (columns: `question`, `answer`)

See the [datasets reference](datasets.md#registered-datasets) for complete details.

## Column Specification

The `column_spec` parameter defines how dataset items map to function arguments:

### Simple Mapping

```python
# Dataset: [("What is 2+2?", "4"), ("What is 3+3?", "6")]
@foreach("question,answer", math_dataset)
def eval_math(question, answer, model):
    # question gets "What is 2+2?"
    # answer gets "4"
    result = model.solve(question)
    return exact_match(result, answer)
```

### Complex Data Structures

```python
# Dataset with nested data
dataset = [
    {"text": "Hello world", "metadata": {"difficulty": "easy"}, "expected": "greeting"},
    {"text": "Complex text", "metadata": {"difficulty": "hard"}, "expected": "complex"}
]

@foreach("text,expected", dataset)
def eval_classification(text, expected, model):
    # Only extracts 'text' and 'expected' fields
    prediction = model.classify(text)
    return exact_match(prediction, expected)
```

### Multiple Column Formats

```python
# Single column
@foreach("text", text_only_dataset)
def eval_single(text, model):
    return model.process(text)

# Many columns
@foreach("input,expected,context,difficulty", complex_dataset)
def eval_complex(input, expected, context, difficulty, model):
    response = model.generate(input, context=context)
    return context_aware_match(response, expected, difficulty)
```

## Dataset Formats

The `@foreach` decorator works with various dataset formats:

### Python Lists

```python
dataset = [
    ("What is the capital of France?", "Paris"),
    ("What is 2+2?", "4"),
    ("Name a color", "red")
]

@foreach("question,answer", dataset)
def eval_qa(question, answer, model):
    return exact_match(model.answer(question), answer)
```

### Generators

```python
def load_data():
    """Generator that yields data items."""
    with open("dataset.jsonl") as f:
        for line in f:
            item = json.loads(line)
            yield (item["question"], item["answer"])

@foreach("question,answer", load_data())
def eval_from_file(question, answer, model):
    return exact_match(model.answer(question), answer)
```

### Hugging Face Datasets

```python
from datasets import load_dataset

def gsm8k_data():
    """Load and format GSM8K dataset."""
    dataset = load_dataset("gsm8k", "main", split="test", streaming=True)
    for item in dataset:
        question = item["question"]
        # Extract answer from solution text
        answer = extract_answer(item["answer"])
        yield (question, answer)

@foreach("question,answer", gsm8k_data())
def eval_gsm8k(question, answer, model):
    response = model.solve(question)
    return exact_match(response, answer)
```

### Custom Iterators

```python
class CustomDataset:
    def __init__(self, data_path):
        self.data_path = data_path

    def __iter__(self):
        with open(self.data_path) as f:
            for line in f:
                data = json.loads(line)
                yield (data["input"], data["output"])

dataset = CustomDataset("my_data.jsonl")

@foreach("input,output", dataset)
def eval_custom(input, output, model):
    result = model.process(input)
    return exact_match(result, output)
```

## Function Arguments

Decorated functions receive dataset columns plus any additional arguments:

### Fixtures and Dependencies

```python
import pytest

@pytest.fixture
def model():
    """Load model once for all evaluations."""
    return load_expensive_model()

@pytest.fixture
def tokenizer():
    """Load tokenizer."""
    return load_tokenizer()

@foreach("text,label", dataset)
def eval_with_fixtures(text, label, model, tokenizer):
    """Function receives dataset columns + fixtures."""
    tokens = tokenizer.encode(text)
    prediction = model.classify(tokens)
    return exact_match(prediction, label)
```

### Additional Parameters

```python
@foreach("question,answer", dataset)
def eval_with_params(question, answer, model, temperature=0.7, max_tokens=100):
    """Pass additional parameters to control generation."""
    response = model.generate(
        question,
        temperature=temperature,
        max_tokens=max_tokens
    )
    return exact_match(response, answer)

# Call with custom parameters
eval_with_params(model=my_model, temperature=0.5, max_tokens=50)
```

## Integration with pytest

The `@foreach` decorator creates functions that work seamlessly with pytest:

### Basic pytest Integration

```python
# test_evaluation.py
import pytest
from doteval import foreach

@pytest.fixture
def model():
    return load_model()

@foreach("prompt,expected", test_data)
def test_model_accuracy(prompt, expected, model):
    """This becomes a pytest test automatically."""
    result = model.generate(prompt)
    return exact_match(result, expected)
```

Run with pytest:

```bash
# Run the evaluation as a test
pytest test_evaluation.py::test_model_accuracy --session my_eval

# With custom parameters
pytest test_evaluation.py --session my_eval --samples 100
```

### Multiple Evaluations

```python
@foreach("question,answer", math_dataset)
def test_math_reasoning(question, answer, model):
    """Test mathematical reasoning."""
    return math_evaluator(model.solve(question), answer)

@foreach("text,sentiment", sentiment_dataset)
def test_sentiment_analysis(text, sentiment, model):
    """Test sentiment classification."""
    return exact_match(model.classify(text), sentiment)

@foreach("prompt,response", creative_dataset)
def test_creative_writing(prompt, response, model):
    """Test creative writing quality."""
    generated = model.write(prompt)
    return creativity_score(generated, response)
```

## Execution Modes

Functions decorated with `@foreach` can be executed in different ways.

### Direct Function Call

You can call a function decorated with `@foreach` directly:

```python
@foreach("text,label", dataset)
def eval_function(text, label, model):
    return exact_match(model.classify(text), label)

# Call directly as a regular function
model = load_model()
results = eval_function(model=model)
print(results.summary)  # EvaluationSummary object
```

### pytest Test Execution

Evaluation functions named with the prefix `eval_` are recognized by pytest and executed. Unlike `@pytest.mark.parametrize`, `@foreach` does not create a test case per element. You can otherwise use every pytest construct and command line option:

```bash
# Run as pytest test with session management
pytest eval_file.py::eval_function --session my_evaluation
```

### Programmatic Execution

You can run the evaluations programatically without using the `@foreach` decorator:

```python
from doteval.core import run_evaluation

results = run_evaluation(
    eval_fn=eval_function,
    column_spec=column_spec,
    dataset=dataset,
    model=my_model,
    max_concurrency=10,
    samples=100
)
```

## Advanced Features

### Custom Retry Configuration

Configure retry behavior for handling transient failures:

```python
from tenacity import AsyncRetrying, stop_after_attempt, wait_exponential, retry_if_exception_type
from doteval import ForEach
import aiohttp

# Custom retry strategy for API calls
api_retries = AsyncRetrying(
    retry=retry_if_exception_type((aiohttp.ClientError, TimeoutError)),
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=1, min=4, max=60)
)

# Create ForEach instance with custom retries
foreach = ForEach(retries=api_retries)

@foreach("prompt,expected", dataset)
async def eval_api_model(prompt, expected, api_model):
    """Evaluation with automatic retries on API errors."""
    response = await api_model.generate(prompt)  # Will retry up to 5 times
    return exact_match(response, expected)
```

### Custom Concurrency Strategies

Control how evaluations are executed:

```python
from doteval import ForEach
from doteval.concurrency import SlidingWindowStrategy, BatchStrategy, SequentialStrategy

# For async functions - sliding window concurrency
sliding_window = SlidingWindowStrategy(max_concurrency=20)
foreach_async = ForEach(concurrency=sliding_window)

@foreach_async("text,label", large_dataset)
async def eval_high_concurrency(text, label, model):
    """Run up to 20 evaluations concurrently."""
    response = await model.classify(text)
    return exact_match(response, label)

# For sync functions - batch processing
batch_strategy = BatchStrategy(batch_size=50)
foreach_batch = ForEach(concurrency=batch_strategy)

@foreach_batch("text,label", dataset)
def eval_in_batches(text, label, model):
    """Process evaluations in batches of 50."""
    response = model.classify(text)
    return exact_match(response, label)

# For sync functions - sequential processing (default)
sequential = SequentialStrategy()
foreach_seq = ForEach(concurrency=sequential)
```

### Implementing Custom Concurrency Strategies

Create your own concurrency strategy:

```python
from doteval.concurrency import AsyncConcurrencyStrategy
import asyncio
from typing import AsyncIterator, Callable, TypeVar

T = TypeVar('T')

class RateLimitedStrategy:
    """Custom strategy with rate limiting."""

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
            done, pending = await asyncio.wait(pending, return_when=asyncio.FIRST_COMPLETED)
            for completed in done:
                result = await completed
                if progress_callback:
                    progress_callback(result)
                yield result

# Use the custom strategy
rate_limited = RateLimitedStrategy(max_concurrency=10, requests_per_second=5)
foreach = ForEach(concurrency=rate_limited)
```

### Complete Configuration Example

Combine retry, concurrency, and storage configuration:

```python
from tenacity import AsyncRetrying, stop_after_attempt, wait_fixed
from doteval import ForEach
from doteval.concurrency import SlidingWindowStrategy
from doteval.storage import SQLiteStorage

# Configure all aspects
foreach = ForEach(
    retries=AsyncRetrying(stop=stop_after_attempt(3), wait=wait_fixed(2)),
    concurrency=SlidingWindowStrategy(max_concurrency=10),
    storage=SQLiteStorage("results.db"),
    name="api_evaluation"
)

@foreach("prompt,expected", test_prompts)
async def eval_with_full_config(prompt, expected, api_client):
    """Evaluation with retry, concurrency, and storage configuration."""
    response = await api_client.complete(prompt)
    return exact_match(response, expected)
```

### Async Evaluations

To be able to run evaluations concurrently you need to provide an async function:

```python
import asyncio

@foreach("prompt,expected", async_dataset)
async def eval_async_model(prompt, expected, async_model):
    """Async evaluation for better throughput."""
    response = await async_model.generate_async(prompt)
    return exact_match(response, expected)

# Run with controlled concurrency
# pytest eval_async.py --session async_eval --max-concurrency 20
```

### Error Handling

The decorator automatically handles errors in evaluation functions:

```python
@foreach("question,answer", dataset)
def eval_with_errors(question, answer, model):
    """Evaluation that might fail on some inputs."""
    try:
        # Complex processing that might fail
        processed_question = preprocess(question)
        response = model.generate(processed_question)
        return exact_match(response, answer)
    except Exception as e:
        # Errors are automatically caught and logged
        # Evaluation continues with next item
        raise e  # Re-raise to be handled by framework
```

### Multiple Return Values

Return multiple evaluation results from a single function:

```python
@foreach("text,expected_sentiment,expected_topic", dataset)
def eval_multi_task(text, expected_sentiment, expected_topic, model):
    """Evaluate multiple aspects of model output."""
    result = model.analyze(text)

    sentiment_score = exact_match(result.sentiment, expected_sentiment)
    topic_score = exact_match(result.topic, expected_topic)
    confidence_score = confidence_evaluator(result.confidence)

    return sentiment_score, topic_score, confidence_score
```

## Session Management Integration

The decorator automatically integrates with doteval's session management:

### Automatic Resume

```python
@foreach("question,answer", large_dataset)
def eval_large_dataset(question, answer, model):
    """Large evaluation that might be interrupted."""
    response = model.generate(question)
    return exact_match(response, answer)

# If interrupted, running again automatically resumes:
# pytest eval_large.py::eval_large_dataset --session large_eval
```

## Performance Optimization

### Limiting Dataset Size

When running evaluations on large datasets it can be useful to test the evaluation function with a few samples at a time. The number of samples can be set from the command line with the `--samples` option.

```python
# Limit dataset for testing
@foreach("question,answer", large_dataset)
def eval_small_test(question, answer, model):
    """Test with subset of data."""
    return exact_match(model.answer(question), answer)

# Or use command-line option:
# pytest eval.py --session test --samples 100
```

### Concurrency Control

You can set the maximum number of concurrent requests from the command line with the `--max-concurrency` option:

```python
@foreach("prompt,expected", dataset)
async def eval_concurrent(prompt, expected, async_model):
    """Async evaluation with automatic concurrency control."""
    response = await async_model.generate_async(prompt)
    return exact_match(response, expected)

# Control concurrency via command line:
# pytest eval.py --session eval --max-concurrency 50
```

### Memory Optimization

`@foreach` is designed with streaming in mind, which is useful for instance when your dataset is too big to fit in memory:

```python
def streaming_dataset():
    """Generator to avoid loading entire dataset in memory."""
    with open("large_file.jsonl") as f:
        for line in f:
            item = json.loads(line)
            yield (item["input"], item["output"])

@foreach("input,output", streaming_dataset())
def eval_memory_efficient(input, output, model):
    """Process one item at a time."""
    result = model.process(input)
    return exact_match(result, output)
```
