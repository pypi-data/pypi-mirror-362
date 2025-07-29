# Data Handling

doteval provides flexible data handling capabilities that support various dataset formats and sources, making it easy to work with different types of evaluation data.

## Overview

doteval supports:

- Multiple dataset formats (lists, tuples, iterators, generators)
- Built-in registered datasets with `@foreach.dataset_name()` syntax
- HuggingFace Datasets integration
- Custom column mappings
- Streaming datasets for large-scale evaluations
- Dynamic dataset generation

## Basic Dataset Formats

### Simple Lists and Tuples

The most basic format uses lists of tuples:

```python
import doteval
from doteval.evaluators import exact_match

# Simple question-answer pairs
dataset = [
    ("What is 2+2?", "4"),
    ("What is 3+3?", "6"),
    ("What is the capital of France?", "Paris")
]

@doteval.foreach("question,answer", dataset)
def eval_simple(question, answer):
    result = model.generate(question)
    return exact_match(result, answer)
```

### Single Column Datasets

For datasets with single values:

```python
# Single column dataset
prompts = [("Write a poem",), ("Explain gravity",), ("Tell a joke",)]

@doteval.foreach("prompt", prompts)
def eval_single_column(prompt):
    result = model.generate(prompt)
    return quality_score(result)
```

### Multi-Column Datasets

For complex datasets with multiple columns:

```python
# Multi-column dataset
dataset = [
    ("context1", "question1", "answer1", "metadata1"),
    ("context2", "question2", "answer2", "metadata2"),
]

@doteval.foreach("context,question,answer,metadata", dataset)
def eval_multi_column(context, question, answer, metadata):
    prompt = f"Context: {context}\nQuestion: {question}"
    result = model.generate(prompt)
    return exact_match(result, answer)
```

## Registered Datasets

doteval includes built-in support for popular evaluation datasets through a simple registry system. These datasets are available using the `@foreach.dataset_name()` syntax and handle all the data loading and preprocessing automatically.

### GSM8K Dataset

GSM8K is a dataset of grade school math word problems with step-by-step reasoning.

```python
from doteval import foreach
from doteval.evaluators import numeric_match

@foreach.gsm8k("test")
def eval_math_reasoning(question, reasoning, answer, model):
    """Evaluate model on GSM8K math problems."""
    response = model.solve(question)
    return numeric_match(response, answer)

# The dataset provides three columns:
# - question: The math word problem
# - reasoning: The step-by-step solution
# - answer: The final numeric answer

# You can also use different splits
@foreach.gsm8k("train")
def eval_math_training(question, reasoning, answer, model):
    # Use reasoning for few-shot prompting
    prompt = f"Problem: {question}\nShow your work step by step."
    response = model.solve(prompt)
    return numeric_match(response, answer)
```

#### Using GSM8K Reasoning for Few-Shot Prompting

The reasoning column contains step-by-step solutions which can be used for few-shot prompting:

```python
import itertools
from doteval.datasets.gsm8k import GSM8K
from doteval.evaluators import numeric_match

# Load training examples for few-shot prompting
train_dataset = GSM8K("train")
few_shot_examples = [
    {"question": q, "reasoning": r, "answer": a}
    for q, r, a in itertools.islice(train_dataset, 3)  # Get 3 examples
]

@foreach.gsm8k("test")
def eval_with_reasoning(question, reasoning, answer, model):
    # Build few-shot prompt with reasoning examples
    prompt = "Solve these math problems step by step:\n\n"

    for ex in few_shot_examples:
        prompt += f"Q: {ex['question']}\n"
        prompt += f"A: {ex['reasoning']}\n"
        prompt += f"#### {ex['answer']}\n\n"

    prompt += f"Q: {question}\nA: "

    response = model.generate(prompt)
    # Extract numeric answer from response
    return numeric_match(response, answer)
```

### BFCL Dataset

BFCL (Berkeley Function Calling Leaderboard) is a comprehensive dataset for evaluating models' function calling capabilities. The dataset tests whether models can correctly select and invoke functions with appropriate parameters based on user queries.

```python
from doteval import foreach
from doteval.evaluators import exact_match

@foreach.bfcl("simple")
def eval_function_calling(question, schema, answer, model):
    """Evaluate model on function calling tasks."""
    # Generate function call based on question and available functions
    response = model.generate_function_call(
        user_query=question,
        available_functions=schema
    )

    # Compare with expected function call
    return exact_match(response, answer)

# The dataset provides three columns:
# - question: The user's natural language query
# - schema: JSON string of available function definitions
# - answer: JSON string of expected function call(s) with parameters
```

#### BFCL Variants

BFCL supports three variants for different function calling scenarios:

```python
# Simple function calling - single function selection
@foreach.bfcl("simple")
def eval_simple(question, schema, answer, model):
    # Model needs to call one function with correct parameters
    pass

# Multiple function calling - select from multiple available functions
@foreach.bfcl("multiple")
def eval_multiple(question, schema, answer, model):
    # Model needs to select the right function from multiple options
    pass

# Parallel function calling - multiple function invocations
@foreach.bfcl("parallel")
def eval_parallel(question, schema, answer, model):
    # Model needs to make multiple function calls in parallel
    pass
```

#### Working with BFCL Data

The schema and answer fields are JSON strings that need to be parsed:

```python
import json
from doteval import foreach
<<<<<<< HEAD

@foreach.bfcl("simple")
def eval_with_parsing(question, schema, answer, model):
    # Parse the function schemas
    available_functions = json.loads(schema)

    # Generate function call
    response = model.generate_function_call(
        question,
        functions=available_functions
    )

    # Parse expected answer
    expected_calls = json.loads(answer)

    # Custom evaluation logic
    if response == expected_calls:
        return Score(value=1.0, passed=True)
    else:
        return Score(value=0.0, passed=False)
```

### SROIE Dataset

SROIE (Scanned Receipts OCR and Information Extraction) is a dataset for testing the ability of models to extract key information from digitized receipts. The dataset is sourced from the [ICDAR 2019 SROIE competition](https://github.com/zzzDavid/ICDAR-2019-SROIE) and contains 626 annotated receipt images.

```python
from doteval import foreach
from doteval.evaluators import exact_match, valid_json

@foreach.sroie()
def eval_receipt_extraction(image, expected_info, model):
    """Evaluate model on receipt information extraction."""
    # Extract information from the receipt image
    extracted_info = model.extract_receipt_info(image)

    # Check if the output is valid JSON
    if not valid_json(extracted_info):
        return Score(value=0.0, passed=False)

    # Compare extracted info with expected
    return exact_match(extracted_info, expected_info)

# The dataset provides two columns:
# - image: PIL Image object of the receipt
# - expected_info: JSON string with company, date, address, and total fields
```

#### Working with SROIE Images

The SROIE dataset provides PIL Image objects that can be used with multimodal models:
from doteval.evaluators import exact_match

```python
import json
from doteval import foreach
@foreach.sroie()
def eval_multimodal_extraction(image, expected_info, multimodal_model):
    """Use a multimodal model to extract receipt information."""
    # Use a multimodal model to analyze the receipt
    prompt = """Extract the following information from this receipt:
    - company: The company/store name
    - date: The transaction date
    - address: The store address
    - total: The total amount

    Return as JSON with these exact keys."""

    response = multimodal_model.generate(prompt, image=image)

    # Parse and validate the response
    try:
        extracted = json.loads(response)
        # Ensure all required fields are present
        required_fields = {"company", "date", "address", "total"}
        if not all(field in extracted for field in required_fields):
            return Score(value=0.0, passed=False)

        # Normalize to match expected format
        extracted_json = json.dumps(extracted, sort_keys=True)
        return exact_match(extracted_json, expected_info)
    except json.JSONDecodeError:
        return Score(value=0.0, passed=False)
```

### Available Registered Datasets

The following datasets are available through the registry:

- **gsm8k**: Grade school math problems (columns: `question`, `reasoning`, `answer`)
- **bfcl**: Berkeley Function Calling Leaderboard (columns: `question`, `schema`, `answer`)
  - Variants: `simple`, `multiple`, `parallel`
- **sroie**: Receipt information extraction (columns: `image`, `expected_info`)

### Listing Available Datasets

You can discover available datasets programmatically:

```python
from doteval.datasets import list_available

# List all registered datasets
available_datasets = list_available()
print(available_datasets)  # ['bfcl', 'gsm8k', 'sroie']

# Get information about a specific dataset
from doteval.datasets import get_dataset_info
info = get_dataset_info('gsm8k')
print(f"Columns: {info['columns']}")  # ['question', 'reasoning', 'answer']
print(f"Splits: {info['splits']}")    # ['train', 'test']
```

### Creating Custom Dataset Classes

You can create your own registered datasets by extending the `Dataset` base class:

```python
from doteval.datasets.base import Dataset, _registry
import re
from typing import Iterator

class MyCustomDataset(Dataset):
    name = "my_custom"
    splits = ["train", "test"]
    columns = ["input", "output"]

    def __init__(self, split: str, **kwargs):
        # Load your dataset and set num_rows
        self.data = load_my_data(split)
        self.num_rows = len(self.data)

    def __iter__(self) -> Iterator[tuple[str, str]]:
        for item in self.data:
            yield (item["input"], item["output"])

# Register your dataset
_registry.register(MyCustomDataset)

# Now you can use it
@foreach.my_custom("test")
def eval_my_dataset(input_text, output, model):
    result = model.generate(input_text)
    return exact_match(result, output)
```

### Direct Execution

Registered dataset functions can be called directly outside of pytest:

```python
# Direct execution - you need to provide fixtures yourself
@foreach.gsm8k("test")
def eval_gsm8k(question, reasoning, answer, model, template):
    prompt = template(question=question)
    result = model.generate(prompt)
    return numeric_match(result, answer)

# Call directly with manual fixtures
result = eval_gsm8k(model=my_model, template=my_template)
print(f"Accuracy: {result.accuracy}")
```

### Progress Bars and Metadata

Registered datasets automatically provide:

- **Progress bars** with dataset name and total count
- **Live metrics** during evaluation
- **Dataset size detection** for accurate progress tracking

```bash
✨ GSM8K [1,319 examples] ━━━━━━━━━━ 1319/1319 • Elapsed: 0:05:23 • ETA: 0:00:00
Accuracy: 73.2%
```

## HuggingFace Datasets Integration

!!! note "Optional Dependency"
    To use HuggingFace Datasets integration, you need to install the `datasets` library:
    ```bash
    pip install datasets
    ```

### Loading Standard Datasets

```python
import datasets
import itertools
from typing import Optional

# Note: The built-in GSM8K dataset already handles parsing reasoning and answer.
# This example shows how to load datasets manually if needed.

def load_custom_dataset(split: str, limit: Optional[int] = None):
    """Load a custom dataset from HuggingFace."""
    dataset = datasets.load_dataset(
        path="your_dataset",
        name="main",
        split=split,
        streaming=True
    )

    # Convert to tuples matching your evaluation needs
    samples = ((sample["input"], sample["output"]) for sample in dataset)

    if limit:
        samples = itertools.islice(samples, limit)

    return samples

@doteval.foreach("input,output", load_custom_dataset("test", 100))
def eval_custom(input_text, output):
    result = model.generate(input_text)
    return exact_match(result, output)
```

### Custom Dataset Loading

```python
def load_custom_dataset(path: str):
    """Load custom dataset from JSON file."""
    import json

    with open(path) as f:
        data = json.load(f)

    return [(item["input"], item["expected"]) for item in data]

@doteval.foreach("input,expected", load_custom_dataset("my_dataset.json"))
def eval_custom(input_text, expected):
    result = model.generate(input_text)
    return exact_match(result, expected)
```

## Streaming and Generators

### Generator Functions

Use generators for memory-efficient dataset processing:

```python
def generate_math_problems(count: int):
    """Generate math problems on-the-fly."""
    import random

    for i in range(count):
        a = random.randint(1, 100)
        b = random.randint(1, 100)
        question = f"What is {a} + {b}?"
        answer = str(a + b)
        yield (question, answer)

@doteval.foreach("question,answer", generate_math_problems(1000))
def eval_generated_math(question, answer):
    result = model.generate(question)
    return exact_match(result, answer)
```

### Streaming Large Datasets

```python
def stream_large_dataset(file_path: str):
    """Stream dataset from large file."""
    import csv

    with open(file_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            yield (row["prompt"], row["expected"])

@doteval.foreach("prompt,expected", stream_large_dataset("large_dataset.csv"))
def eval_streamed(prompt, expected):
    result = model.generate(prompt)
    return exact_match(result, expected)
```

## Column Specification

### Column Mapping

Map dataset columns to function parameters:

```python
# Dataset with different column names
dataset = [
    ("Tell me about cats", "Cats are mammals..."),
    ("Explain photosynthesis", "Photosynthesis is...")
]

@doteval.foreach("user_prompt,expected_response", dataset)
def eval_with_mapping(user_prompt, expected_response):
    result = model.generate(user_prompt)
    return similarity_score(result, expected_response)
```

### Flexible Column Order

Column order must match the dataset structure:

```python
# Dataset: (context, question, answer, difficulty)
dataset = [
    ("The sky is blue.", "What color is the sky?", "blue", "easy"),
    ("E=mc²", "What is Einstein's equation?", "E=mc²", "medium")
]

# Column spec must match dataset order
@doteval.foreach("context,question,answer,difficulty", dataset)
def eval_ordered(context, question, answer, difficulty):
    prompt = f"Context: {context}\nQuestion: {question}"
    result = model.generate(prompt)

    score = exact_match(result, answer)
    score.metadata["difficulty"] = difficulty
    return score
```

## Dataset Transformations

### Data Preprocessing

```python
def preprocess_dataset(raw_dataset):
    """Clean and transform dataset."""
    processed = []

    for item in raw_dataset:
        # Clean text
        question = item["question"].strip()
        answer = item["answer"].lower().strip()

        # Skip invalid entries
        if not question or not answer:
            continue

        processed.append((question, answer))

    return processed

@doteval.foreach("question,answer", preprocess_dataset(raw_data))
def eval_preprocessed(question, answer):
    result = model.generate(question)
    return exact_match(result, answer)
```

### Data Augmentation

```python
def augment_dataset(base_dataset, augment_count=2):
    """Augment dataset with variations."""
    augmented = []

    for question, answer in base_dataset:
        # Original item
        augmented.append((question, answer))

        # Augmented versions
        for i in range(augment_count):
            aug_question = rephrase(question)
            augmented.append((aug_question, answer))

    return augmented

@doteval.foreach("question,answer", augment_dataset(base_data))
def eval_augmented(question, answer):
    result = model.generate(question)
    return exact_match(result, answer)
```

## Sampling and Filtering

### Random Sampling

```python
import random

def sample_dataset(dataset, sample_size: int, seed: int = 42):
    """Randomly sample from dataset."""
    random.seed(seed)
    dataset_list = list(dataset)
    return random.sample(dataset_list, min(sample_size, len(dataset_list)))

@doteval.foreach("question,answer", sample_dataset(large_dataset, 100))
def eval_sampled(question, answer):
    result = model.generate(question)
    return exact_match(result, answer)
```

### Stratified Sampling

```python
def stratified_sample(dataset, strata_column: str, samples_per_stratum: int):
    """Sample evenly across different strata."""
    from collections import defaultdict

    strata = defaultdict(list)

    for item in dataset:
        stratum = item[strata_column]
        strata[stratum].append(item)

    sampled = []
    for stratum_data in strata.values():
        sampled.extend(random.sample(stratum_data,
                                   min(samples_per_stratum, len(stratum_data))))

    return sampled
```

### Filtering

```python
def filter_dataset(dataset, min_length: int = 10):
    """Filter dataset based on criteria."""
    return [
        (question, answer)
        for question, answer in dataset
        if len(question) >= min_length and len(answer) >= min_length
    ]

@doteval.foreach("question,answer", filter_dataset(raw_dataset))
def eval_filtered(question, answer):
    result = model.generate(question)
    return exact_match(result, answer)
```

## Complex Dataset Patterns

### Nested Data Structures

```python
# Complex nested data
complex_dataset = [
    {
        "id": "q1",
        "conversation": [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi there!"}
        ],
        "metadata": {"difficulty": "easy"}
    }
]

def flatten_conversations(dataset):
    """Flatten complex dataset structure."""
    flattened = []

    for item in dataset:
        conversation = item["conversation"]
        user_msg = next(msg["content"] for msg in conversation if msg["role"] == "user")
        assistant_msg = next(msg["content"] for msg in conversation if msg["role"] == "assistant")

        flattened.append((user_msg, assistant_msg, item["metadata"]["difficulty"]))

    return flattened

@doteval.foreach("user_input,expected_output,difficulty", flatten_conversations(complex_dataset))
def eval_conversations(user_input, expected_output, difficulty):
    result = model.generate(user_input)
    return exact_match(result, expected_output)
```

### Multi-Turn Conversations

```python
def prepare_multi_turn_dataset(conversations):
    """Prepare multi-turn conversation dataset."""
    dataset = []

    for conv in conversations:
        context = []

        for i, turn in enumerate(conv["turns"]):
            if turn["role"] == "user":
                context.append(f"User: {turn['content']}")
                if i + 1 < len(conv["turns"]):
                    expected = conv["turns"][i + 1]["content"]
                    context_str = "\n".join(context)
                    dataset.append((context_str, expected))
                    context.append(f"Assistant: {expected}")

    return dataset

@doteval.foreach("context,expected_response", prepare_multi_turn_dataset(conversations))
def eval_multi_turn(context, expected_response):
    result = model.generate(context)
    return similarity_score(result, expected_response)
```

## Data Validation

### Schema Validation

```python
def validate_dataset_schema(dataset, required_columns: list):
    """Validate dataset has required structure."""
    for i, item in enumerate(dataset):
        if len(item) != len(required_columns):
            raise ValueError(f"Item {i} has {len(item)} columns, expected {len(required_columns)}")

        for j, value in enumerate(item):
            if not isinstance(value, str):
                raise ValueError(f"Item {i}, column {j} is not a string")

    return dataset

# Validate before evaluation
validated_dataset = validate_dataset_schema(raw_dataset, ["question", "answer"])

@doteval.foreach("question,answer", validated_dataset)
def eval_validated(question, answer):
    result = model.generate(question)
    return exact_match(result, answer)
```

### Data Quality Checks

```python
def check_data_quality(dataset):
    """Check dataset quality and report issues."""
    issues = []

    for i, (question, answer) in enumerate(dataset):
        if not question.strip():
            issues.append(f"Empty question at index {i}")

        if not answer.strip():
            issues.append(f"Empty answer at index {i}")

        if len(question) < 5:
            issues.append(f"Very short question at index {i}")

    if issues:
        print("Data quality issues found:")
        for issue in issues[:10]:  # Show first 10 issues
            print(f"  - {issue}")

    return dataset

@doteval.foreach("question,answer", check_data_quality(dataset))
def eval_quality_checked(question, answer):
    result = model.generate(question)
    return exact_match(result, answer)
```

## Performance Considerations

### Memory-Efficient Processing

```python
# Use generators for large datasets
def memory_efficient_loader(file_path: str):
    """Load large dataset without loading everything into memory."""
    import json

    with open(file_path) as f:
        for line in f:
            item = json.loads(line)  # JSONL format
            yield (item["question"], item["answer"])

@doteval.foreach("question,answer", memory_efficient_loader("large_dataset.jsonl"))
def eval_memory_efficient(question, answer):
    result = model.generate(question)
    return exact_match(result, answer)
```

### Caching Expensive Operations

```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def expensive_preprocessing(text: str) -> str:
    """Cache expensive preprocessing operations."""
    # Expensive text processing
    return processed_text

def cached_dataset_loader(base_dataset):
    """Use caching for expensive preprocessing."""
    for question, answer in base_dataset:
        processed_question = expensive_preprocessing(question)
        processed_answer = expensive_preprocessing(answer)
        yield (processed_question, processed_answer)

@doteval.foreach("question,answer", cached_dataset_loader(raw_dataset))
def eval_cached(question, answer):
    result = model.generate(question)
    return exact_match(result, answer)
```

## Best Practices

### Dataset Organization

```python
# Organize datasets by evaluation type
def load_evaluation_dataset(eval_type: str, split: str = "test"):
    """Load dataset for specific evaluation type."""
    datasets = {
        "math": load_gsm8k_dataset,
        "reasoning": load_reasoning_dataset,
        "coding": load_coding_dataset,
    }

    if eval_type not in datasets:
        raise ValueError(f"Unknown evaluation type: {eval_type}")

    return datasets[eval_type](split)

@doteval.foreach("question,answer", load_evaluation_dataset("math"))
def eval_math(question, answer):
    result = model.generate(question)
    return exact_match(result, answer)
```

### Error Handling

```python
def robust_dataset_loader(source):
    """Load dataset with robust error handling."""
    for i, item in enumerate(source):
        try:
            if isinstance(item, dict):
                yield (item["question"], item["answer"])
            else:
                yield item
        except (KeyError, IndexError, TypeError) as e:
            print(f"Skipping malformed item at index {i}: {e}")
            continue

@doteval.foreach("question,answer", robust_dataset_loader(messy_data))
def eval_robust(question, answer):
    result = model.generate(question)
    return exact_match(result, answer)
```

### Reproducibility

```python
def reproducible_dataset(base_dataset, seed: int = 42):
    """Ensure reproducible dataset ordering."""
    import random

    # Convert to list and sort for consistency
    dataset_list = sorted(list(base_dataset))

    # Shuffle with fixed seed for reproducible randomness
    random.seed(seed)
    random.shuffle(dataset_list)

    return dataset_list

@doteval.foreach("question,answer", reproducible_dataset(dataset))
def eval_reproducible(question, answer):
    result = model.generate(question)
    return exact_match(result, answer)
```
