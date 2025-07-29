# Sessions

Sessions in doteval provide robust state management for evaluations, enabling progress tracking, interruption recovery, and result persistence. They ensure that no evaluation work is ever lost, even in the face of system crashes or network failures.

## Overview

A session represents a complete evaluation run with:
- **Unique identification** via session names
- **Progress tracking** of which items have been processed
- **Result persistence** across process restarts
- **Automatic resumption** from where evaluations left off
- **Error recovery** with selective retry of failed items

## Session Lifecycle

Sessions progress through distinct states that determine their behavior:

### Session States

#### Running
- **Description**: Evaluation is currently in progress by an active process
- **CLI Display**: "Running"
- **Resumable**: No (already active)
- **Lock Status**: Locked

```bash
# Active evaluation in progress
pytest eval_math.py --session math_eval
# Session shows as "Running" while pytest is executing
```

#### Interrupted
- **Description**: Process crashed or was killed before evaluation completed
- **CLI Display**: "Interrupted"
- **Resumable**: Yes (resumes from last completed item)
- **Lock Status**: Locked (stale lock from crashed process)

```bash
# Process was killed mid-evaluation
doteval list
# Shows: math_eval | Interrupted | 2024-01-15 14:30:22

# Resume from where it left off
pytest eval_math.py --session math_eval
```

#### Has errors
- **Description**: Evaluation finished but some items failed with errors
- **CLI Display**: "Has errors"
- **Resumable**: Yes (retries only failed items)
- **Lock Status**: Locked (available for retry)

```bash
# Some items failed during evaluation
doteval list
# Shows: math_eval | Has errors | 2024-01-15 14:30:22

# Retry only the failed items
pytest eval_math.py --session math_eval
```

#### Completed
- **Description**: Evaluation finished successfully with all items processed
- **CLI Display**: "Completed"
- **Resumable**: No (evaluation is finished)
- **Lock Status**: Unlocked

```bash
# All items processed successfully
doteval list
# Shows: math_eval | Completed | 2024-01-15 14:30:22

# Cannot resume completed sessions
pytest eval_math.py --session math_eval
# Error: Session 'math_eval' is already completed
```

## Session Management

### Creating Sessions

Sessions are created automatically when you run an evaluation:

```python
@foreach("question,answer", dataset)
def eval_math(question, answer):
    response = model.generate(question)
    return exact_match(response, answer)

# Run with session - creates session if it doesn't exist
pytest eval_math.py --session math_baseline
```

### Resuming Sessions

Resumption works automatically by using the same session name:

```python
# Original run (gets interrupted)
pytest eval_large.py --session large_eval --samples 500

# Resume later - continues from item 501
pytest eval_large.py --session large_eval --samples 1000
```

### Session Data

Each session stores:

```python
from doteval.sessions import SessionManager

manager = SessionManager("json://evals")
session = manager.get_session("my_evaluation")

print(f"Session: {session.name}")
print(f"Status: {session.status}")
print(f"Created: {session.created_at}")
print(f"Results: {len(session.results)} evaluations")

# Access specific evaluation results
math_results = session.results["eval_math"]
print(f"Math eval: {len(math_results)} items")
```

## Advanced Session Features

### Incremental Processing

Use the `samples` parameter for incremental processing of large datasets:

```bash
# Process first 1000 items
pytest eval_massive.py --session massive_eval --samples 1000
# Session remains "Running" (not completed)

# Later: process 2000 more items (total 3000)
pytest eval_massive.py --session massive_eval --samples 3000
# Processes items 1001-3000 only

# Finally: process entire dataset
pytest eval_massive.py --session massive_eval
# Processes remaining items and marks as "Completed"
```

!!! info "Session Completion Logic"
    - With `--samples`: Session stays "Running" for continuation
    - Without `--samples`: Session marked "Completed" when done

### Error Recovery

Sessions with errors can be selectively retried:

```python
@foreach("question,answer", dataset)
def eval_with_possible_errors(question, answer):
    try:
        response = unreliable_model.generate(question)
        return exact_match(response, answer)
    except APIError:
        raise  # This item will be marked as failed
```

```bash
# Initial run - some items fail
pytest eval_unreliable.py --session recovery_test
# Session status: "Has errors"

# View which items failed
doteval show recovery_test --full | grep '"error"'

# Retry only failed items
pytest eval_unreliable.py --session recovery_test
# Only items with errors are retried
```

### Progress Tracking

Sessions track completion at the item level:

```python
from doteval.sessions import SessionManager

manager = SessionManager("json://evals")
session = manager.get_session("my_session")

# Get completed item IDs for specific evaluation
completed_ids = session.get_completed_item_ids("eval_math")
print(f"Completed items: {completed_ids}")

# Check if specific item was completed
if 42 in completed_ids:
    print("Item 42 was successfully processed")
```

## Session Configuration

### Storage Location

Configure where sessions are stored:

```bash
# Default location
pytest eval.py --session test  # Uses json://evals

# Custom location
pytest eval.py --session test --storage "json://my_evaluations"

# Absolute path
pytest eval.py --session test --storage "json:///home/user/experiments"
```

### Session Naming

Choose meaningful session names for organization:

```bash
# Include date/version in name
pytest eval.py --session "gpt4_baseline_2024_01_15"

# Use environment/config info
pytest eval.py --session "prod_config_gsm8k_v2"

# Experiment tracking
pytest eval.py --session "exp_${EXPERIMENT_ID}_temperature_0_7"
```

### Concurrent Access

Sessions are protected against concurrent access:

```bash
# Terminal 1
pytest eval.py --session shared_session
# Acquires lock

# Terminal 2 (same time)
pytest eval.py --session shared_session
# Error: Session is currently being used by another process
```

## Session Patterns

### Development Workflow

```bash
# Quick test during development
pytest eval.py --session dev_test --samples 10
doteval show dev_test

# Iterate on evaluation logic
pytest eval.py --session dev_test --samples 10  # Retries same 10 items
doteval delete dev_test  # Clean up when done
```

### Production Evaluation

```bash
# Full production run
pytest eval_production.py --session "prod_run_$(date +%Y%m%d)"

# Monitor progress
doteval list --name "prod_run"

# View results
doteval show "prod_run_$(date +%Y%m%d)"
```

### Batch Experiments

```bash
# Run multiple configurations
for temp in 0.1 0.5 0.9; do
    pytest eval_temp.py --session "temp_${temp}" --temperature $temp
done

# Compare results
for temp in 0.1 0.5 0.9; do
    echo "Temperature $temp:"
    doteval show "temp_${temp}"
done
```

### Long-running Evaluations

```bash
# Start large evaluation
pytest eval_massive.py --session massive_2024 &
EVAL_PID=$!

# Monitor in another terminal
watch "doteval list --name massive"

# If process gets killed, resume
pytest eval_massive.py --session massive_2024
```

## Session Storage Format

Sessions are stored in JSON format with the following structure:

```json
{
  "name": "math_evaluation",
  "status": "Completed",
  "created_at": 1705325422.123,
  "metadata": {
    "git_commit": "a1b2c3d4"
  },
  "results": {
    "eval_math": [
      {
        "scores": [
          {
            "name": "exact_match",
            "value": true,
            "metrics": ["accuracy"],
            "metadata": {"prediction": "42", "expected": "42"}
          }
        ],
        "item_id": 0,
        "item_data": {"question": "What is 6*7?", "answer": "42"},
        "error": null,
        "timestamp": 1705325422.456
      }
    ]
  }
}
```

## Lock Files

Lock files prevent concurrent access and detect interruptions:

```bash
# Lock file created when session starts
ls evals/
# math_eval.json      # Session data
# math_eval.lock      # Lock file (only while running)
```

Lock file behavior:
- **Created**: When session starts
- **Removed**: When session completes successfully
- **Kept**: When session fails or is interrupted
- **Detected**: Used to identify interrupted sessions

## Troubleshooting

### Session Not Found

```bash
$ doteval show my_session
Session 'my_session' not found

# Check available sessions
$ doteval list
```

### Cannot Resume Completed Session

```bash
$ pytest eval.py --session completed_session
Error: Session 'completed_session' is already completed. Use a different session name.

# Use a new session name for new evaluation
$ pytest eval.py --session completed_session_v2
```

### Session Locked by Another Process

```bash
$ pytest eval.py --session active_session
Error: Session 'active_session' is currently being used by another process.

# Wait for other process to finish, or check if it's a stale lock
$ ps aux | grep pytest
$ doteval list --name active_session
```

### Corrupted Session Data

```bash
# If session file is corrupted
$ doteval show corrupted_session
Error: Failed to load session 'corrupted_session': Invalid JSON

# Recovery options:
# 1. Delete corrupted session and start fresh
$ doteval delete corrupted_session

# 2. Manually fix JSON file
$ vim evals/corrupted_session.json

# 3. Restore from backup if available
$ cp evals/backups/corrupted_session.json evals/
```

### Stale Lock Files

```bash
# If process crashed, lock file may remain
$ doteval list
# Shows: old_session | Interrupted | 2024-01-10 10:00:00

# Resume will clear stale lock
$ pytest eval.py --session old_session

# Or manually remove lock file
$ rm evals/old_session.lock
```

## Best Practices

### Session Naming

- Use descriptive names: `gpt4_gsm8k_baseline` not `test1`
- Include dates for experiments: `model_eval_2024_01_15`
- Use consistent naming schemes across projects
- Avoid special characters that might cause filesystem issues

### Session Organization

```bash
# Use subdirectories for organization
pytest eval.py --session exp1 --storage "json://experiments/model_comparison"
pytest eval.py --session exp2 --storage "json://experiments/prompt_optimization"

# Regular cleanup of old sessions
doteval list | grep "2023-" | xargs -I {} doteval delete {}
```

### Error Handling

```python
@foreach("question,answer", dataset)
def robust_evaluation(question, answer):
    try:
        response = model.generate(question)
        return exact_match(response, answer)
    except Exception as e:
        # Log error but don't crash entire evaluation
        logging.error(f"Failed on question {question}: {e}")
        raise  # Re-raise to mark item as failed
```

### Performance Optimization

```bash
# Use appropriate concurrency for your API limits
pytest eval_api.py --session api_eval --max-concurrency 5

# Process in batches for very large datasets
pytest eval_huge.py --session huge_eval --samples 10000
pytest eval_huge.py --session huge_eval --samples 20000
# Continue until complete...
pytest eval_huge.py --session huge_eval  # Process remainder
```

Sessions provide the foundation for reliable, resumable evaluations in doteval. By understanding session states and lifecycle, you can build robust evaluation pipelines that handle interruptions gracefully and never lose progress.
