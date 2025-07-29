"""Tests for BFCL dataset loader."""

import json
import os
import tempfile
from unittest.mock import patch

import pytest

from doteval.datasets.base import _registry
from doteval.datasets.bfcl import BFCL


def test_bfcl_dataset_attributes():
    """Test BFCL dataset has correct attributes."""
    assert BFCL.name == "bfcl"
    assert BFCL.variants == ["simple", "multiple", "parallel"]
    assert BFCL.columns == ["question", "schema", "answer"]


def test_bfcl_auto_registration():
    """Test BFCL dataset is automatically registered."""
    assert "bfcl" in _registry.list_datasets()
    dataset_class = _registry.get_dataset_class("bfcl")
    assert dataset_class == BFCL


def test_bfcl_invalid_variant():
    """Test BFCL raises error for invalid variant."""
    with pytest.raises(ValueError, match="Variant 'invalid' not supported"):
        BFCL(variant="invalid")


@patch("urllib.request.urlretrieve")
def test_bfcl_download_and_merge(mock_urlretrieve):
    """Test BFCL dataset download and data merging."""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create mock question data
        question_data = [
            {
                "id": "simple_0",
                "question": [
                    [{"role": "user", "content": "Calculate the area of a triangle"}]
                ],
                "function": [
                    {"name": "calculate_area", "parameters": {"base": "number"}}
                ],
            },
            {
                "id": "simple_1",
                "question": [[{"role": "user", "content": "Get weather information"}]],
                "function": [{"name": "get_weather", "parameters": {"city": "string"}}],
            },
        ]

        # Create mock answer data
        answer_data = [
            {
                "id": "simple_0",
                "ground_truth": [{"calculate_area": {"base": [10], "height": [5]}}],
            },
            {
                "id": "simple_1",
                "ground_truth": [{"get_weather": {"city": ["New York"]}}],
            },
        ]

        # Mock urlretrieve to create test files
        def mock_urlretrieve_side_effect(url, path):
            if "possible_answer" in url:
                # Write answer file
                with open(path, "w") as f:
                    for item in answer_data:
                        f.write(json.dumps(item) + "\n")
            else:
                # Write question file
                with open(path, "w") as f:
                    for item in question_data:
                        f.write(json.dumps(item) + "\n")

        mock_urlretrieve.side_effect = mock_urlretrieve_side_effect

        # Patch mkdtemp to use our test directory
        with patch("tempfile.mkdtemp", return_value=temp_dir):
            dataset = BFCL(variant="simple")

            # Check dataset attributes
            assert dataset.num_rows == 2
            assert dataset.variant == "simple"

            # Test iteration
            results = list(dataset)
            assert len(results) == 2

            # Check first item
            question, schema, answer = results[0]
            assert question == "Calculate the area of a triangle"
            assert "calculate_area" == schema[0]["properties"]["function"]["const"]
            assert "calculate_area" in answer[0]

            # Check second item
            question, schema, answer = results[1]
            assert question == "Get weather information"
            assert "get_weather" == schema[0]["properties"]["function"]["const"]
            assert "get_weather" in answer[0]


@patch("urllib.request.urlretrieve")
def test_bfcl_different_variants(mock_urlretrieve):
    """Test loading different BFCL variants."""

    def mock_urlretrieve_side_effect(url, path):
        # Create empty but valid JSON files
        with open(path, "w") as f:
            f.write("")

    mock_urlretrieve.side_effect = mock_urlretrieve_side_effect

    for variant in ["simple", "multiple", "parallel"]:
        with patch("tempfile.mkdtemp", return_value=tempfile.mkdtemp()):
            dataset = BFCL(variant=variant)
            assert dataset.variant == variant

            # Verify correct URLs were called
            calls = mock_urlretrieve.call_args_list[-2:]  # Last 2 calls
            question_url = calls[0][0][0]
            answer_url = calls[1][0][0]

            assert f"BFCL_v3_{variant}.json" in question_url
            assert f"possible_answer/BFCL_v3_{variant}.json" in answer_url


@patch("urllib.request.urlretrieve", side_effect=Exception("Download failed"))
def test_bfcl_download_failure(mock_urlretrieve):
    """Test BFCL behavior when download fails."""
    with pytest.raises(RuntimeError, match="Failed to download BFCL dataset"):
        BFCL(variant="simple")


def test_bfcl_cleanup():
    """Test that BFCL cleans up temporary directory."""
    with patch("urllib.request.urlretrieve"):
        # Create valid JSONL files when urlretrieve is called
        def mock_urlretrieve(url, path):
            with open(path, "w") as f:
                # Write valid JSONL format (one JSON object per line)
                if "possible_answer" in url:
                    f.write('{"id": "test_0", "ground_truth": [{"func": {}}]}\n')
                else:
                    f.write(
                        '{"id": "test_0", "question": [[{"role": "user", "content": "test"}]], "function": [{"name": "func"}]}\n'
                    )

        with patch("urllib.request.urlretrieve", side_effect=mock_urlretrieve):
            dataset = BFCL(variant="simple")
            temp_dir = dataset.temp_dir

            # Directory should exist
            assert os.path.exists(temp_dir)

            # Delete the dataset
            del dataset

            # Directory should be cleaned up
            assert not os.path.exists(temp_dir)


@patch("urllib.request.urlretrieve")
def test_bfcl_complex_question_format(mock_urlretrieve):
    """Test BFCL handles complex question formats correctly."""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Test different question formats
        question_data = [
            {
                "id": "test_0",
                "question": [[{"role": "user", "content": "Normal question"}]],
                "function": [{"name": "func1"}],
            },
            {
                "id": "test_1",
                "question": [[]],  # Empty conversation
                "function": [{"name": "func2"}],
            },
            {
                "id": "test_2",
                "question": [],  # No conversation
                "function": [{"name": "func3"}],
            },
        ]

        answer_data = [
            {"id": "test_0", "ground_truth": [{"func1": {}}]},
            {"id": "test_1", "ground_truth": [{"func2": {}}]},
            {"id": "test_2", "ground_truth": [{"func3": {}}]},
        ]

        def mock_urlretrieve_side_effect(url, path):
            if "possible_answer" in url:
                with open(path, "w") as f:
                    for item in answer_data:
                        f.write(json.dumps(item) + "\n")
            else:
                with open(path, "w") as f:
                    for item in question_data:
                        f.write(json.dumps(item) + "\n")

        mock_urlretrieve.side_effect = mock_urlretrieve_side_effect

        with patch("tempfile.mkdtemp", return_value=temp_dir):
            dataset = BFCL(variant="simple")
            results = list(dataset)

            assert len(results) == 3
            # Check that empty questions are handled gracefully
            assert results[0][0] == "Normal question"
            assert results[1][0] == ""  # Empty conversation
            assert results[2][0] == ""  # No conversation
