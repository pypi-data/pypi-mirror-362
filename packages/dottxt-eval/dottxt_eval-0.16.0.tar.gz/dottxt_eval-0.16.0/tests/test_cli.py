"""Tests for the CLI."""

import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest
from click.testing import CliRunner

from doteval.cli import cli
from doteval.metrics import accuracy
from doteval.models import Evaluation, EvaluationStatus, Record, Result, Score
from doteval.storage import JSONStorage


@pytest.fixture
def cli_runner():
    """Provide a CLI test runner."""
    return CliRunner()


@pytest.fixture
def temp_storage():
    """Provide temporary storage for CLI tests."""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield Path(temp_dir)


def test_cli_list_empty_storage(cli_runner):
    """Test 'doteval list' with empty storage."""
    with patch("doteval.cli.get_storage") as mock_get_storage:
        mock_storage = mock_get_storage.return_value
        mock_storage.list_experiments.return_value = []

        result = cli_runner.invoke(cli, ["list"])

        assert result.exit_code == 0
        assert "No experiments found" in result.output


def test_cli_list_with_experiments(cli_runner):
    """Test 'doteval list' with existing experiments."""
    with patch("doteval.cli.get_storage") as mock_get_storage:
        mock_storage = mock_get_storage.return_value
        mock_storage.list_experiments.return_value = ["exp1", "exp2"]
        mock_storage.list_evaluations.side_effect = [
            ["eval1", "eval2"],  # exp1 has 2 evaluations
            ["eval3"],  # exp2 has 1 evaluation
        ]

        result = cli_runner.invoke(cli, ["list"])

        assert result.exit_code == 0
        assert "exp1" in result.output
        assert "exp2" in result.output
        assert "2" in result.output  # exp1 has 2 evaluations
        assert "1" in result.output  # exp2 has 1 evaluation


def test_cli_show_existing_experiment(cli_runner):
    """Test 'doteval show' with existing experiment."""
    with patch("doteval.cli.get_storage") as mock_get_storage:
        mock_storage = mock_get_storage.return_value
        mock_storage.list_experiments.return_value = ["test_exp"]
        mock_storage.list_evaluations.return_value = ["eval1"]

        # Create mock results
        score = Score("test_evaluator", 0.95, [], {})
        result = Result(score, prompt="test")
        record = Record(result=result, item_id=0, dataset_row={})

        mock_storage.get_results.return_value = [record]

        result = cli_runner.invoke(cli, ["show", "test_exp"])

        assert result.exit_code == 0
        assert "test_exp" in result.output
        assert "eval1" in result.output


def test_cli_show_nonexistent_experiment(cli_runner):
    """Test 'doteval show' with nonexistent experiment."""
    with patch("doteval.cli.get_storage") as mock_get_storage:
        mock_storage = mock_get_storage.return_value
        mock_storage.list_experiments.return_value = []

        result = cli_runner.invoke(cli, ["show", "nonexistent"])

        assert result.exit_code == 0  # CLI doesn't exit with error code
        assert "not found" in result.output


def test_cli_rename_experiment_success(cli_runner):
    """Test 'doteval rename' command success."""
    with patch("doteval.cli.get_storage") as mock_get_storage:
        mock_storage = mock_get_storage.return_value
        mock_storage.list_experiments.return_value = ["old_name"]

        result = cli_runner.invoke(cli, ["rename", "old_name", "new_name"])

        assert result.exit_code == 0
        assert "renamed" in result.output
        mock_storage.rename_experiment.assert_called_once_with("old_name", "new_name")


def test_cli_rename_nonexistent_experiment(cli_runner):
    """Test 'doteval rename' with nonexistent experiment."""
    with patch("doteval.cli.get_storage") as mock_get_storage:
        mock_storage = mock_get_storage.return_value
        mock_storage.list_experiments.return_value = []

        result = cli_runner.invoke(cli, ["rename", "nonexistent", "new_name"])

        assert result.exit_code == 0
        assert "not found" in result.output


def test_cli_delete_experiment_success(cli_runner):
    """Test 'doteval delete' command success."""
    with patch("doteval.cli.get_storage") as mock_get_storage:
        mock_storage = mock_get_storage.return_value
        mock_storage.list_experiments.return_value = ["exp_to_delete"]

        result = cli_runner.invoke(cli, ["delete", "exp_to_delete"])

        assert result.exit_code == 0
        assert "Deleted experiment" in result.output
        mock_storage.delete_experiment.assert_called_once_with("exp_to_delete")


def test_cli_delete_nonexistent_experiment(cli_runner):
    """Test 'doteval delete' with nonexistent experiment."""
    with patch("doteval.cli.get_storage") as mock_get_storage:
        mock_storage = mock_get_storage.return_value
        mock_storage.list_experiments.return_value = []

        result = cli_runner.invoke(cli, ["delete", "nonexistent"])

        assert result.exit_code == 0
        assert "not found" in result.output


def test_cli_list_with_name_filter(cli_runner):
    """Test 'doteval list --name' filtering."""
    with patch("doteval.cli.get_storage") as mock_get_storage:
        mock_storage = mock_get_storage.return_value
        mock_storage.list_experiments.return_value = [
            "math_eval",
            "text_eval",
            "other_test",
        ]
        mock_storage.list_evaluations.return_value = []

        result = cli_runner.invoke(cli, ["list", "--name", "eval"])

        assert result.exit_code == 0
        # Should only show experiments containing "eval"
        assert "math_eval" in result.output
        assert "text_eval" in result.output
        # The name filter should prevent "other_test" from being in output


def test_cli_show_with_full_flag(cli_runner):
    """Test 'doteval show --full' with detailed output."""
    with patch("doteval.cli.get_storage") as mock_get_storage:
        mock_storage = mock_get_storage.return_value
        mock_storage.list_experiments.return_value = ["test_exp"]
        mock_storage.list_evaluations.return_value = ["eval1"]

        # Create mock results
        score = Score("test_evaluator", 0.95, [], {})
        result = Result(score, prompt="test")
        record = Record(result=result, item_id=0, dataset_row={})

        mock_storage.get_results.return_value = [record]

        result = cli_runner.invoke(cli, ["show", "test_exp", "--full"])

        assert result.exit_code == 0
        # With --full flag, should show JSON output
        assert "json" in result.output.lower() or "{" in result.output


def test_cli_with_custom_storage_option(cli_runner):
    """Test CLI commands with custom storage option."""
    with patch("doteval.cli.get_storage") as mock_get_storage:
        mock_storage = mock_get_storage.return_value
        mock_storage.list_experiments.return_value = []

        result = cli_runner.invoke(cli, ["list", "--storage", "json://custom/path"])

        # Should pass custom storage path to get_storage
        mock_get_storage.assert_called_with("json://custom/path")
        assert result.exit_code == 0


def test_cli_show_with_errors(cli_runner):
    """Test 'doteval show' displays error counts."""
    with patch("doteval.cli.get_storage") as mock_get_storage:
        mock_storage = mock_get_storage.return_value
        mock_storage.list_experiments.return_value = ["test_exp"]
        mock_storage.list_evaluations.return_value = ["eval_test"]

        # Create mock results with some errors
        accuracy_metric = accuracy()
        results = [
            Record(
                result=Result(
                    Score("llm_judge", 0.9, [accuracy_metric], {}), prompt="test1"
                ),
                item_id=1,
                dataset_row={"prompt": "test1"},
                error=None,
                timestamp=1640995200.0,
            ),
            Record(
                result=Result(Score("llm_judge", 0, [accuracy_metric], {}), prompt=""),
                item_id=2,
                dataset_row={"prompt": "test2"},
                error="ConnectionError: Unable to connect to API",
                timestamp=1640995201.0,
            ),
            Record(
                result=Result(
                    Score("llm_judge", 0.8, [accuracy_metric], {}), prompt="test3"
                ),
                item_id=3,
                dataset_row={"prompt": "test3"},
                error=None,
                timestamp=1640995202.0,
            ),
            Record(
                result=Result(Score("llm_judge", 0, [accuracy_metric], {}), prompt=""),
                item_id=4,
                dataset_row={"prompt": "test4"},
                error="ValueError: Invalid response format",
                timestamp=1640995203.0,
            ),
        ]

        mock_storage.get_results.return_value = results

        result = cli_runner.invoke(cli, ["show", "test_exp"])

        assert result.exit_code == 0
        # Check that error count is displayed
        assert "2/4 (50.0%)" in result.output
        # Check error summary section
        assert "Error Summary:" in result.output
        assert "Total errors: 2 out of 4 items" in result.output
        assert "ConnectionError: 1 occurrence" in result.output
        assert "ValueError: 1 occurrence" in result.output


def test_show_command_with_no_evaluations():
    """Test show command when experiment has no evaluations."""
    runner = CliRunner()

    with tempfile.TemporaryDirectory() as temp_dir:
        # Create an experiment without evaluations
        storage = JSONStorage(temp_dir)
        storage.create_experiment("empty_exp")

        result = runner.invoke(
            cli, ["show", "empty_exp", "--storage", f"json://{temp_dir}"]
        )
        assert result.exit_code == 0
        assert "No evaluations found for experiment 'empty_exp'" in result.output


def test_show_command_with_specific_evaluation_not_found():
    """Test show command when specific evaluation is not found."""
    runner = CliRunner()

    with tempfile.TemporaryDirectory() as temp_dir:
        # Create an experiment with one evaluation
        storage = JSONStorage(temp_dir)
        storage.create_experiment("test_exp")
        eval1 = Evaluation(
            evaluation_name="eval1",
            status=EvaluationStatus.COMPLETED,
            started_at=1234567890,
        )
        storage.create_evaluation("test_exp", eval1)

        result = runner.invoke(
            cli,
            [
                "show",
                "test_exp",
                "--evaluation",
                "nonexistent",
                "--storage",
                f"json://{temp_dir}",
            ],
        )
        assert result.exit_code == 0
        assert "Evaluation 'nonexistent' not found" in result.output


def test_show_command_with_errors_flag():
    """Test show command with --errors flag to show error details."""
    runner = CliRunner()

    with tempfile.TemporaryDirectory() as temp_dir:
        # Create experiment with evaluation containing errors
        storage = JSONStorage(temp_dir)
        storage.create_experiment("error_exp")
        eval1 = Evaluation(
            evaluation_name="error_eval",
            status=EvaluationStatus.COMPLETED,
            started_at=1234567890,
        )
        storage.create_evaluation("error_exp", eval1)

        # Add results with errors
        result1 = Result(prompt="test1")
        record1 = Record(
            result=result1,
            item_id=0,
            dataset_row={
                "input": "This is a very long input that should be truncated when displayed in the CLI output to ensure it doesn't take up too much space"
            },
            error="ValueError: Test error 1",
            timestamp=1234567890,
        )

        result2 = Result(prompt="test2")
        record2 = Record(
            result=result2,
            item_id=1,
            dataset_row={"input": "short input"},
            error="KeyError: Test error 2",
            timestamp=1234567891,
        )

        storage.add_results("error_exp", "error_eval", [record1, record2])

        result = runner.invoke(
            cli, ["show", "error_exp", "--errors", "--storage", f"json://{temp_dir}"]
        )
        assert result.exit_code == 0
        assert "Error Details (2 errors):" in result.output
        assert "ValueError: Test error 1" in result.output
        assert "KeyError: Test error 2" in result.output
        assert "..." in result.output  # Check truncation


def test_rename_command_with_existing_new_name():
    """Test rename command when new name already exists."""
    runner = CliRunner()

    with tempfile.TemporaryDirectory() as temp_dir:
        # Create two experiments
        storage = JSONStorage(temp_dir)
        storage.create_experiment("exp1")
        storage.create_experiment("exp2")

        result = runner.invoke(
            cli, ["rename", "exp1", "exp2", "--storage", f"json://{temp_dir}"]
        )
        assert result.exit_code == 0
        assert "Experiment 'exp2' already exists" in result.output


def test_delete_command_with_error():
    """Test delete command when storage raises an error."""
    runner = CliRunner()

    with tempfile.TemporaryDirectory() as temp_dir:
        # Create an experiment
        storage = JSONStorage(temp_dir)
        storage.create_experiment("test_exp")

        # Mock storage to raise an error
        with patch.object(
            JSONStorage, "delete_experiment", side_effect=Exception("Storage error")
        ):
            result = runner.invoke(
                cli, ["delete", "test_exp", "--storage", f"json://{temp_dir}"]
            )
            assert result.exit_code == 0
            assert "Error deleting experiment: Storage error" in result.output


def test_show_command_with_zero_accuracy_and_errors():
    """Test show command with zero accuracy excluding errors."""
    runner = CliRunner()

    with tempfile.TemporaryDirectory() as temp_dir:
        storage = JSONStorage(temp_dir)
        storage.create_experiment("test_exp")
        eval1 = Evaluation(
            evaluation_name="test_eval",
            status=EvaluationStatus.COMPLETED,
            started_at=1234567890,
        )
        storage.create_evaluation("test_exp", eval1)

        # Add results: all false scores plus some errors
        acc_metric = accuracy()

        results = []
        # Add false results
        for i in range(3):
            result = Result(
                Score("evaluator1", False, [acc_metric], {}), prompt=f"test{i}"
            )
            record = Record(result=result, item_id=i, dataset_row={})
            results.append(record)

        # Add error results
        for i in range(3, 5):
            result = Result(prompt=f"test{i}")
            record = Record(
                result=result, item_id=i, dataset_row={}, error="Test error"
            )
            results.append(record)

        storage.add_results("test_exp", "test_eval", results)

        result = runner.invoke(
            cli, ["show", "test_exp", "--storage", f"json://{temp_dir}"]
        )
        assert result.exit_code == 0
        # Check that it shows accuracy with and without errors
        assert "0.00 (0.00 excluding errors)" in result.output


def test_list_command_filters_by_name():
    """Test list command with name filter."""
    runner = CliRunner()

    with tempfile.TemporaryDirectory() as temp_dir:
        storage = JSONStorage(temp_dir)
        # Create multiple experiments
        storage.create_experiment("test_exp_1")
        storage.create_experiment("test_exp_2")
        storage.create_experiment("other_exp")

        # List with filter
        result = runner.invoke(
            cli, ["list", "--name", "test", "--storage", f"json://{temp_dir}"]
        )
        assert result.exit_code == 0
        assert "test_exp_1" in result.output
        assert "test_exp_2" in result.output
        assert "other_exp" not in result.output
