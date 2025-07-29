# Command Line Interface

The doteval CLI provides powerful tools for managing evaluation sessions, viewing results, and monitoring progress.

## Installation

The CLI is included when you install doteval:

```bash
pip install doteval
```

Verify installation:

```bash
doteval --help
```

## Core Commands

### `doteval list`

List all available evaluation sessions.

```bash
doteval list
```

**Options:**

- `--name TEXT` - Filter sessions by name (partial match)
- `--status [Running|Completed|Has errors|Interrupted]` - Filter by session status
- `--storage TEXT` - Storage backend path (default: `json://evals`)

**Examples:**

```bash
# List all sessions
doteval list

# Filter by name
doteval list --name "gsm8k"

# Filter by status
doteval list --status "Completed"

# Filter by both name and status
doteval list --name "math" --status "Running"

# Use custom storage location
doteval list --storage "json://my_evals"
```

**Sample Output:**

```
┌─────────────────────┬─────────────┬─────────────────────┐
│ Session Name        │ Status      │ Created             │
├─────────────────────┼─────────────┼─────────────────────┤
│ gsm8k_baseline      │ Completed   │ 2024-01-15 14:30:22 │
│ gsm8k_improved      │ Running     │ 2024-01-15 16:45:10 │
│ gpqa_evaluation     │ Has errors  │ 2024-01-14 09:15:33 │
│ custom_eval_test    │ Interrupted │ 2024-01-13 11:20:15 │
└─────────────────────┴─────────────┴─────────────────────┘
```

### `doteval show`

Display detailed information about a specific session.

```bash
doteval show SESSION_NAME
```

**Options:**

- `--storage TEXT` - Storage backend path (default: `json://evals`)
- `--full` - Show complete session data in JSON format

**Examples:**

```bash
# Show session summary
doteval show gsm8k_baseline

# Show full session details
doteval show gsm8k_baseline --full

# Show session from custom storage
doteval show my_eval --storage "json://custom_path"
```

**Sample Output (Summary):**

```
::gsm8k_baseline:eval_gsm8k
┌────────────┬──────────┬───────┐
│ Evaluator  │ Metric   │ Score │
├────────────┼──────────┼───────┤
│ exact_match│ accuracy │  0.73 │
└────────────┴──────────┴───────┘
```

**Sample Output (Full):**

```json
{
  "name": "gsm8k_baseline",
  "status": "Completed",
  "created_at": 1705325422.123,
  "results": {
    "eval_gsm8k": [
      {
        "scores": [
          {
            "name": "exact_match",
            "value": true,
            "metrics": ["accuracy"],
            "metadata": {"value": "42", "expected": "42"}
          }
        ],
        "item_id": 0,
        "input_data": {"question": "What is 6*7?", "answer": "42"}
      }
    ]
  }
}
```

### `doteval rename`

Rename an existing evaluation session.

```bash
doteval rename OLD_NAME NEW_NAME
```

**Options:**

- `--storage TEXT` - Storage backend path (default: `json://evals`)

**Examples:**

```bash
# Rename a session
doteval rename old_experiment new_experiment

# Rename with custom storage
doteval rename exp1 experiment_v2 --storage "json://my_evals"
```

### `doteval delete`

Delete an evaluation session permanently.

```bash
doteval delete SESSION_NAME
```

**Options:**

- `--storage TEXT` - Storage backend path (default: `json://evals`)

**Examples:**

```bash
# Delete a session
doteval delete failed_experiment

# Delete from custom storage
doteval delete old_eval --storage "json://archived_evals"
```

!!! warning "Permanent Deletion"
    This action cannot be undone. All evaluation results for the session will be permanently lost.

## Session Status

Sessions can have the following statuses:

- **Running** - Evaluation is currently in progress by an active process
- **Completed** - Evaluation finished successfully (cannot be resumed)
- **Has errors** - Evaluation finished but some items failed (can be resumed to retry failed items)
- **Interrupted** - Evaluation process crashed or was killed before completion (can be resumed)

## Storage Backends

doteval supports different storage backends for evaluation data:

### JSON Storage (Default)

```bash
# Default location
doteval list --storage "json://evals"

# Custom directory
doteval list --storage "json://my_custom_path"

# Absolute path
doteval list --storage "json:///home/user/evaluations"
```

The JSON storage backend stores each session as a separate JSON file in the specified directory.

## Working with pytest

The CLI integrates seamlessly with pytest for running evaluations:

### Basic Evaluation

```bash
# Run evaluation with session name
pytest eval_gsm8k.py --session my_gsm8k_eval

# Run with custom storage
pytest eval_gsm8k.py --session my_eval --storage json://custom_path
```

### Resuming Interrupted Evaluations

If an evaluation is interrupted, it can be resumed by running the same command:

```bash
# This will automatically resume from where it left off
pytest eval_gsm8k.py --session my_gsm8k_eval
```

### Resuming Sessions with Errors

Sessions that finished with errors can also be resumed to retry only the failed items:

```bash
# Check which sessions have errors
doteval list --status "Has errors"

# Resume the session - will only retry items that failed
pytest eval_gsm8k.py --session my_gsm8k_eval
```

When resuming an error session:
- ✅ Items that completed successfully are skipped
- 🔄 Items that failed are retried
- 📊 All results (old and new) are preserved in the same session

### Concurrent Evaluations

Control concurrency for async evaluations:

```bash
pytest eval_async.py --session async_eval --max-concurrency 20
```

### Retry Configuration

Configure retry behavior for handling transient failures:

```bash
# Set maximum retry attempts (default: 3)
pytest eval_api.py --session api_eval --max-retries 5

# Set retry delay in seconds (default: 1.0)
pytest eval_api.py --session api_eval --retry-delay 2.0

# Combine retry options
pytest eval_api.py --session api_eval --max-retries 10 --retry-delay 5.0
```

**Note**: These options apply to the default retry behavior for connection errors. For more advanced retry configuration, use the `ForEach` class with custom `AsyncRetrying` instances.

### Sample Limits

Limit the number of samples for testing or incremental processing:

```bash
# Process only 100 items for quick testing
pytest eval_gsm8k.py --session test_run --samples 100

# Process 500 items, then later continue with more
pytest eval_large_dataset.py --session incremental_eval --samples 500
# Later: resume and process more items
pytest eval_large_dataset.py --session incremental_eval --samples 1000
```

!!! info "Session Completion with Samples"
    When using `--samples`, the session remains in "Running" status and can be resumed to process more items. Only evaluations that process the complete dataset (without `--samples`) are marked as "Completed".

## Examples and Workflows

### Daily Evaluation Workflow

```bash
# 1. Run your evaluation
pytest eval_model.py --session "model_v2_$(date +%Y%m%d)"

# 2. Check results
doteval show "model_v2_$(date +%Y%m%d)"

# 3. Compare with previous runs
doteval list --name "model_v2"

# 4. Clean up old experiments
doteval delete "model_v2_20240101"
```

### Batch Processing

```bash
# Run multiple evaluations
for dataset in gsm8k gpqa mmlu; do
    pytest "eval_${dataset}.py" --session "experiment_${dataset}"
done

# View all results
for dataset in gsm8k gpqa mmlu; do
    echo "=== $dataset ==="
    doteval show "experiment_${dataset}"
done
```

### Development Testing

```bash
# Quick test with limited samples
pytest eval_new_feature.py --session dev_test --samples 10

# Check if it worked
doteval show dev_test

# Clean up
doteval delete dev_test
```

## Configuration

### Environment Variables

You can set default values using environment variables:

```bash
export DOTEVAL_STORAGE="json://my_default_path"
export DOTEVAL_MAX_CONCURRENCY=50

# Now these are the defaults
doteval list  # Uses json://my_default_path
pytest eval.py --session test  # Uses 50 max concurrency
```

### Config Files

Create a `.doteval.toml` config file in your project root:

```toml
[doteval]
storage = "json://evaluations"
max_concurrency = 25

[doteval.sessions]
auto_cleanup_days = 30
```

## Troubleshooting

### Common Issues

#### Session Not Found
```bash
doteval show my_session
# Error: Session 'my_session' not found
```
**Solution**: Check available sessions with `doteval list` and verify the session name.

#### Storage Access Error
```bash
doteval list --storage "json://restricted_path"
# Error: Permission denied
```
**Solution**: Ensure you have read/write permissions to the storage directory.

#### Interrupted Session
```bash
doteval list
# Shows session as "Interrupted"
```
**Solution**: Resume by running the original pytest command again.

### Debug Mode

Enable verbose output for debugging:

```bash
# Enable debug logging
export DOTEVAL_DEBUG=1
doteval show my_session

# Or use pytest verbose mode
pytest eval.py --session test -v
```

### Getting Help

```bash
# General help
doteval --help

# Command-specific help
doteval list --help
doteval show --help
doteval rename --help
doteval delete --help
```
