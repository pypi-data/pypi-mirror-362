import json
import re
from datetime import datetime

import click
from rich import box
from rich.console import Console
from rich.syntax import Syntax
from rich.table import Table

from doteval.models import EvaluationSummary
from doteval.storage import get_storage

console = Console()


@click.group()
def cli():
    """doteval CLI to manage experiments and evaluations."""


@cli.command()
@click.option("--name", help="Filter experiments by name.")
@click.option("--storage", default="json://.doteval", help="Storage backend path")
def list(name, storage):
    """List available experiments"""
    storage_backend = get_storage(storage)
    experiment_names = storage_backend.list_experiments()

    # Separate ephemeral and named experiments
    ephemeral_experiments = []
    named_experiments = []
    ephemeral_pattern = re.compile(r"^\d{8}_\d{6}_[a-f0-9]{8}$")

    for exp_name in experiment_names:
        if exp_name == ".doteval":
            continue
        elif ephemeral_pattern.match(exp_name):
            ephemeral_experiments.append(exp_name)
        else:
            named_experiments.append(exp_name)

    if not named_experiments and not ephemeral_experiments:
        console.print(f"[yellow]No experiments found at {storage}.[/yellow]")
        return

    # Show named experiments first
    if named_experiments:
        table = Table(title="Named Experiments", box=box.SIMPLE)
        table.add_column("Experiment Name")
        table.add_column("Evaluations")

        for experiment_name in sorted(named_experiments):
            if name and name not in experiment_name:
                continue

            evaluations = storage_backend.list_evaluations(experiment_name)
            table.add_row(experiment_name, str(len(evaluations)))

        console.print(table)

    # Show ephemeral experiments
    if ephemeral_experiments:
        ephemeral_table = Table(title="Ephemeral Experiments", box=box.SIMPLE)
        ephemeral_table.add_column("Timestamp")
        ephemeral_table.add_column("Evaluations")

        for experiment_name in sorted(ephemeral_experiments, reverse=True):
            if name and name not in experiment_name:
                continue

            evaluations = storage_backend.list_evaluations(experiment_name)
            # Extract timestamp from path
            timestamp = (
                experiment_name.split("/")[-1]
                if "/" in experiment_name
                else experiment_name
            )
            ephemeral_table.add_row(timestamp, str(len(evaluations)))

        if named_experiments:
            console.print()  # Add spacing
        console.print(ephemeral_table)


@cli.command()
@click.argument("experiment_name")
@click.option("--storage", default="json://.doteval", help="Storage backend path")
@click.option("--evaluation", help="Show specific evaluation results.")
@click.option("--full", is_flag=True, help="Show full details.")
@click.option("--errors", is_flag=True, help="Show detailed error information.")
def show(experiment_name, storage, evaluation, full, errors):
    """Show results of an experiment."""
    storage_backend = get_storage(storage)

    # Check if experiment exists
    experiments = storage_backend.list_experiments()
    if experiment_name not in experiments:
        console.print(f"[red]Experiment '{experiment_name}' not found.[/red]")
        return

    # Get all evaluations for this experiment
    evaluation_names = storage_backend.list_evaluations(experiment_name)

    if not evaluation_names:
        console.print(
            f"[yellow]No evaluations found for experiment '{experiment_name}'.[/yellow]"
        )
        return

    # Filter to specific evaluation if requested
    if evaluation:
        if evaluation not in evaluation_names:
            console.print(
                f"[red]Evaluation '{evaluation}' not found in experiment '{experiment_name}'.[/red]"
            )
            return
        evaluation_names = [evaluation]

    # Process each evaluation
    for eval_name in evaluation_names:
        # Get results for this evaluation
        results = storage_backend.get_results(experiment_name, eval_name)

        if full:
            # Show raw JSON data
            content = json.dumps(
                [
                    {
                        "item_id": r.item_id,
                        "result": {
                            "prompt": r.result.prompt,
                            "scores": [
                                {
                                    "name": s.name,
                                    "value": s.value,
                                    "metrics": [m.__name__ for m in s.metrics],
                                    "metadata": s.metadata,
                                }
                                for s in r.result.scores
                            ],
                        },
                        "dataset_row": r.dataset_row,
                        "error": r.error,
                        "timestamp": r.timestamp,
                    }
                    for r in results
                ],
                indent=2,
            )
            syntax = Syntax(content, "json", theme="monokai", line_numbers=True)
            console.print(f"\n[bold]Evaluation: {eval_name}[/bold]")
            console.print(syntax)
            continue

        # Display summary table
        table = Table(
            title=f"Summary of {experiment_name} :: {eval_name}", box=box.SIMPLE
        )
        table.add_column("Evaluator")
        table.add_column("Metric")
        table.add_column("Score", justify="right")
        table.add_column("Errors", justify="right")

        # Count errors
        total_items = len(results)
        error_count = sum(1 for result in results if result.error is not None)
        error_percentage = (error_count / total_items * 100) if total_items > 0 else 0

        # Create evaluation summary
        summary = EvaluationSummary(results).summary if results else {}

        for evaluator, metrics in summary.items():
            for metric_name, score in metrics.items():
                error_display = f"{error_count}/{total_items} ({error_percentage:.1f}%)"
                if error_count > 0:
                    error_display = f"[red]{error_display}[/red]"
                    # Calculate metric excluding errors
                    successful_results = [r for r in results if r.error is None]
                    if successful_results:
                        # Recompute metric for successful results only
                        successful_summary = EvaluationSummary(
                            successful_results
                        ).summary
                        score_without_errors = successful_summary.get(
                            evaluator, {}
                        ).get(metric_name, 0)
                        score_display = (
                            f"{score:.2f} ({score_without_errors:.2f} excluding errors)"
                        )
                    else:
                        score_display = f"{score:.2f}"
                else:
                    score_display = f"{score:.2f}"
                table.add_row(evaluator, metric_name, score_display, error_display)

        console.print(table)

        # Show error summary if there are errors
        if error_count > 0:
            console.print("\n[bold]Error Summary:[/bold]")
            console.print(
                f"Total errors: [red]{error_count}[/red] out of {total_items} items ({error_percentage:.1f}%)"
            )

            # Group errors by type
            error_types = {}
            for result in results:
                if result.error:
                    # Extract error type from the error message
                    error_type = (
                        result.error.split(":")[0] if ":" in result.error else "Unknown"
                    )
                    error_types[error_type] = error_types.get(error_type, 0) + 1

            if error_types:
                console.print("\nError Types:")
                for error_type, count in sorted(
                    error_types.items(), key=lambda x: x[1], reverse=True
                ):
                    console.print(
                        f" • {error_type}: {count} occurrence{'s' if count > 1 else ''}"
                    )

        # Show detailed errors if --errors flag is used
        if errors and error_count > 0:
            console.print(f"\n[bold]Error Details ({error_count} errors):[/bold]\n")
            error_idx = 0
            for result in results:
                if result.error:
                    error_idx += 1
                    console.print(
                        f"[bold][{error_idx}] Item ID: {result.item_id}[/bold]"
                    )
                    console.print(f"    Error: [red]{result.error}[/red]")

                    # Display dataset row (truncated if too long)
                    dataset_str = str(result.dataset_row)
                    if len(dataset_str) > 100:
                        dataset_str = dataset_str[:97] + "..."
                    console.print(f"    Dataset: {dataset_str}")

                    # Display timestamp
                    timestamp = datetime.fromtimestamp(result.timestamp).strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )
                    console.print(f"    Time: {timestamp}\n")


@cli.command()
@click.argument("old_name")
@click.argument("new_name")
@click.option("--storage", default="json://.doteval", help="Storage backend path")
def rename(old_name: str, new_name: str, storage: str):
    """Rename an experiment."""
    storage_backend = get_storage(storage)

    # Check if experiment exists
    experiments = storage_backend.list_experiments()
    if old_name not in experiments:
        console.print(f"[red]Experiment '{old_name}' not found.[/red]")
        return

    # Check if new name already exists
    if new_name in experiments:
        console.print(f"[red]Experiment '{new_name}' already exists.[/red]")
        return

    storage_backend.rename_experiment(old_name, new_name)
    console.print(f"[green]Experiment '{old_name}' renamed to '{new_name}'[/green]")


@cli.command()
@click.argument("experiment_name")
@click.option("--storage", default="json://.doteval", help="Storage backend path")
def delete(experiment_name, storage):
    """Delete an experiment."""
    storage_backend = get_storage(storage)

    # Check if experiment exists
    experiments = storage_backend.list_experiments()
    if experiment_name not in experiments:
        console.print(
            f"[red]Experiment '{experiment_name}' not found. Run 'doteval list' to list the available experiments.[/red]"
        )
        return

    try:
        storage_backend.delete_experiment(experiment_name)
        console.print(f"[green]Deleted experiment '{experiment_name}'[/green]")
    except Exception as e:
        console.print(f"[red]Error deleting experiment: {e}[/red]")


if __name__ == "__main__":
    cli()
