# Metrics

Metrics aggregate evaluation results to provide meaningful performance measurements. They transform lists of individual evaluation results into single numerical scores that help you understand your model's overall performance.

## How Metrics Work

Metrics are functions that take a list of evaluation results and return a single aggregated score. They are attached to evaluators and computed automatically when evaluations complete.

```python
from doteval.metrics import accuracy

# This metric function receives a list of boolean values
# and returns the percentage that are True
score = accuracy()([True, False, True, True])  # Returns 0.75
```

## Built-in Metrics

### accuracy()

The `accuracy` metric calculates the percentage of correct results. It's the most commonly used metric for classification and exact-match tasks.

```python
from doteval.metrics import accuracy
from doteval.evaluators import evaluator

@evaluator(metrics=accuracy())
def exact_match(predicted: str, expected: str) -> bool:
    """Check exact string match."""
    return predicted.strip() == expected.strip()

# When evaluation runs, accuracy will be computed automatically:
# accuracy([True, False, True, True]) = 0.75 (75% accuracy)
```

**Behavior:**
- Takes a list of boolean values
- Returns the fraction of `True` values
- Returns `0.0` for empty lists
- Range: `[0.0, 1.0]`

## Creating Custom Metrics

Use the `@metric` decorator to create custom aggregation functions.

### Basic Custom Metric

```python
from doteval.metrics import metric
from doteval.evaluators import evaluator

@metric
def error_rate() -> Metric:
    """Calculate the error rate (opposite of accuracy)."""
    def calculate(scores: list[bool]) -> float:
        if len(scores) == 0:
            return 0.0
        return 1.0 - (sum(scores) / len(scores))
    return calculate

@evaluator(metrics=[accuracy(), error_rate()])
def spelling_check(text: str, expected: str) -> bool:
    return text.lower().strip() == expected.lower().strip()
```

### Statistical Metrics

Create metrics that compute statistical measures:

```python
@metric
def precision() -> Metric:
    """Calculate precision for binary classification."""
    def calculate(results: list[bool]) -> float:
        if not results:
            return 0.0

        true_positives = sum(results)
        total_predictions = len(results)
        return true_positives / total_predictions if total_predictions > 0 else 0.0

    return calculate

@metric
def recall() -> Metric:
    """Calculate recall - requires additional context."""
    def calculate(results: list[bool]) -> float:
        # This is a simplified example
        # Real recall calculation would need ground truth context
        return sum(results) / len(results) if results else 0.0

    return calculate

@metric
def f1_score() -> Metric:
    """Calculate F1 score combining precision and recall."""
    def calculate(results: list[bool]) -> float:
        if not results:
            return 0.0

        # Simplified F1 calculation
        precision_val = sum(results) / len(results)
        recall_val = precision_val  # Simplified for example

        if precision_val + recall_val == 0:
            return 0.0
        return 2 * (precision_val * recall_val) / (precision_val + recall_val)

    return calculate

@evaluator(metrics=[precision(), recall(), f1_score()])
def classification_evaluator(predicted: str, actual: str) -> bool:
    return predicted == actual
```

### Numerical Metrics

Handle non-boolean evaluation results:

```python
@metric
def mean_absolute_error() -> Metric:
    """Calculate mean absolute error for numerical predictions."""
    def calculate(errors: list[float]) -> float:
        if not errors:
            return 0.0
        return sum(abs(error) for error in errors) / len(errors)

    return calculate

@metric
def root_mean_square_error() -> Metric:
    """Calculate RMSE for numerical predictions."""
    def calculate(errors: list[float]) -> float:
        if not errors:
            return 0.0
        return (sum(error ** 2 for error in errors) / len(errors)) ** 0.5

    return calculate

@evaluator(metrics=[mean_absolute_error(), root_mean_square_error()])
def numerical_difference(predicted: str, expected: str) -> float:
    """Calculate numerical difference between predictions."""
    try:
        pred_val = float(predicted.strip())
        exp_val = float(expected.strip())
        return abs(pred_val - exp_val)
    except ValueError:
        return float('inf')  # Large error for non-numeric values
```

### Text-based Metrics

Create metrics for text evaluation tasks:

```python
@metric
def average_length() -> Metric:
    """Calculate average length of responses."""
    def calculate(texts: list[str]) -> float:
        if not texts:
            return 0.0
        return sum(len(text) for text in texts) / len(texts)

    return calculate

@metric
def keyword_coverage() -> Metric:
    """Calculate what percentage of responses contain keywords."""
    def calculate(results: list[bool]) -> float:
        if not results:
            return 0.0
        return sum(results) / len(results)

    return calculate

@evaluator(metrics=[average_length()])
def response_length_evaluator(response: str) -> str:
    """Return the response itself for length calculation."""
    return response

@evaluator(metrics=[keyword_coverage()])
def keyword_presence(response: str, keyword: str) -> bool:
    """Check if response contains keyword."""
    return keyword.lower() in response.lower()
```

### Complex Aggregation Metrics

Handle more sophisticated aggregation logic:

```python
@metric
def quartile_performance() -> Metric:
    """Calculate performance by quartiles."""
    def calculate(scores: list[bool]) -> dict:
        if not scores:
            return {"q1": 0.0, "q2": 0.0, "q3": 0.0, "q4": 0.0}

        n = len(scores)
        quartile_size = n // 4

        quartiles = {}
        for i, quartile in enumerate(["q1", "q2", "q3", "q4"]):
            start_idx = i * quartile_size
            end_idx = start_idx + quartile_size if i < 3 else n
            quartile_scores = scores[start_idx:end_idx]
            quartiles[quartile] = sum(quartile_scores) / len(quartile_scores) if quartile_scores else 0.0

        return quartiles

    return calculate

@metric
def any_correct() -> Metric:
    """Return 1.0 if any evaluation is correct, 0.0 otherwise."""
    def calculate(scores: list[bool]) -> float:
        return 1.0 if any(scores) else 0.0

    return calculate

@metric
def all_correct() -> Metric:
    """Return 1.0 if all evaluations are correct, 0.0 otherwise."""
    def calculate(scores: list[bool]) -> float:
        return 1.0 if all(scores) else 0.0

    return calculate
```

## Multiple Metrics per Evaluator

Attach multiple metrics to a single evaluator for comprehensive analysis:

```python
@evaluator(metrics=[accuracy(), error_rate(), any_correct(), all_correct()])
def comprehensive_match(predicted: str, expected: str) -> bool:
    """Evaluate with multiple metrics."""
    return predicted.strip().lower() == expected.strip().lower()

# This will compute all four metrics:
# - accuracy: percentage of correct matches
# - error_rate: percentage of incorrect matches
# - any_correct: 1.0 if at least one match is correct
# - all_correct: 1.0 if all matches are correct
```

## Parameterized Metrics

Create metrics that accept parameters:

```python
@metric
def threshold_accuracy(threshold: float = 0.5) -> Metric:
    """Accuracy for scores above a threshold."""
    def calculate(scores: list[float]) -> float:
        if not scores:
            return 0.0
        above_threshold = [score >= threshold for score in scores]
        return sum(above_threshold) / len(above_threshold)

    return calculate

@metric
def top_k_accuracy(k: int = 3) -> Metric:
    """Accuracy considering top-k predictions."""
    def calculate(rankings: list[int]) -> float:
        if not rankings:
            return 0.0
        correct = [rank <= k for rank in rankings]
        return sum(correct) / len(correct)

    return calculate

# Use with parameters
@evaluator(metrics=[threshold_accuracy(0.8), top_k_accuracy(5)])
def confidence_evaluator(prediction: str, expected: str) -> float:
    # Your evaluation logic that returns a confidence score
    similarity = calculate_similarity(prediction, expected)
    return similarity
```

## Metric Registry

doteval maintains a registry of metrics for serialization and deserialization:

```python
from doteval.metrics import registry

# Built-in metrics are automatically registered
print(registry.keys())  # {'accuracy'}

# Custom metrics are registered when defined
@metric
def my_custom_metric() -> Metric:
    def calculate(scores: list[bool]) -> float:
        return sum(scores) / len(scores) if scores else 0.0
    return calculate

# Now available in registry
print('my_custom_metric' in registry)  # True
```

## Working with Evaluation Results

Metrics receive the raw evaluation results from evaluators:

```python
from doteval import foreach
from doteval.evaluators import evaluator
from doteval.metrics import accuracy

@evaluator(metrics=accuracy())
def sentiment_match(predicted: str, expected: str) -> bool:
    """Simple sentiment matching."""
    return predicted.lower().strip() == expected.lower().strip()

@foreach("text,sentiment", sentiment_dataset)
def eval_sentiment(text, sentiment, model):
    prediction = model.classify_sentiment(text)
    return sentiment_match(prediction, sentiment)

# When evaluation completes:
# 1. sentiment_match returns True/False for each sample
# 2. All boolean results are collected into a list
# 3. accuracy() receives this list: [True, False, True, False, ...]
# 4. accuracy() returns the fraction of True values
```

## Advanced Metric Patterns

### Conditional Metrics

Metrics that behave differently based on input:

```python
@metric
def adaptive_accuracy(easy_weight: float = 1.0, hard_weight: float = 2.0) -> Metric:
    """Weighted accuracy based on difficulty."""
    def calculate(results: list[dict]) -> float:
        if not results:
            return 0.0

        total_weight = 0.0
        correct_weight = 0.0

        for result in results:
            weight = easy_weight if result.get('difficulty') == 'easy' else hard_weight
            total_weight += weight
            if result.get('correct', False):
                correct_weight += weight

        return correct_weight / total_weight if total_weight > 0 else 0.0

    return calculate
```

### Cross-Evaluator Metrics

Metrics that consider results from multiple evaluators:

```python
@metric
def combined_score() -> Metric:
    """Combine multiple evaluation criteria."""
    def calculate(composite_results: list[dict]) -> float:
        if not composite_results:
            return 0.0

        scores = []
        for result in composite_results:
            # Assume result contains scores from multiple evaluators
            accuracy_score = result.get('accuracy', 0.0)
            fluency_score = result.get('fluency', 0.0)
            relevance_score = result.get('relevance', 0.0)

            # Weighted combination
            combined = (0.5 * accuracy_score + 0.3 * fluency_score + 0.2 * relevance_score)
            scores.append(combined)

        return sum(scores) / len(scores)

    return calculate
```
