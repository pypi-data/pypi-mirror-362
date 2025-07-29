"""Tests for the numeric_match evaluator."""

from doteval.evaluators import numeric_match
from doteval.models import Score


class TestNumericMatch:
    """Test cases for numeric_match evaluator."""

    def test_basic_integer_comparison(self):
        """Test basic integer comparisons."""
        score = numeric_match(42, 42)
        assert isinstance(score, Score)
        assert score.value is True
        assert score.name == "numeric_match"

        score = numeric_match(42, 43)
        assert score.value is False

    def test_integer_string_comparison(self):
        """Test comparing integers in string format."""
        assert numeric_match("42", "42").value is True
        assert numeric_match("42", 42).value is True
        assert numeric_match(42, "42").value is True
        assert numeric_match("42", "43").value is False

    def test_float_comparison(self):
        """Test float comparisons."""
        assert numeric_match(3.14, 3.14).value is True
        assert numeric_match("3.14", 3.14).value is True
        assert numeric_match(3.14, "3.14").value is True
        assert numeric_match(3.14, 3.15).value is False

    def test_numbers_with_commas(self):
        """Test numbers with thousand separators."""
        assert numeric_match("1,234", "1234").value is True
        assert numeric_match("1,234,567", "1234567").value is True
        assert numeric_match("1,234.56", "1234.56").value is True
        assert numeric_match("1,234", 1234).value is True

    def test_space_as_thousand_separator(self):
        """Test numbers with spaces as thousand separators."""
        assert numeric_match("1 234", "1234").value is True
        assert numeric_match("1 234 567", "1234567").value is True
        assert numeric_match("1 234.56", "1234.56").value is True
        assert numeric_match("1 234 567.89", "1234567.89").value is True
        # Mixed with other formats
        assert numeric_match("1 234", "1,234").value is True
        assert numeric_match("1 234", "1.234e3").value is True
        # Multiple spaces
        assert numeric_match("1  234", "1234").value is True

    def test_scientific_notation(self):
        """Test scientific notation."""
        assert numeric_match("1.234e3", "1234").value is True
        assert numeric_match("1.234E3", "1234").value is True
        assert numeric_match("1e6", "1000000").value is True
        assert numeric_match("1.5e-2", "0.015").value is True
        assert numeric_match("1.5e-2", 0.015).value is True

    def test_leading_trailing_zeros(self):
        """Test numbers with leading/trailing zeros."""
        assert numeric_match("042", "42").value is True
        assert numeric_match("42.0", "42").value is True
        assert numeric_match("42.00", "42.0").value is True
        assert numeric_match("0.50", "0.5").value is True

    def test_whitespace_handling(self):
        """Test whitespace handling."""
        assert numeric_match(" 42 ", "42").value is True
        assert numeric_match("  42  ", 42).value is True
        assert numeric_match("\t42\n", "42").value is True

    def test_negative_numbers(self):
        """Test negative numbers."""
        assert numeric_match("-42", "-42").value is True
        assert numeric_match("-42", -42).value is True
        assert numeric_match("-3.14", "-3.14").value is True
        assert numeric_match("-1,234", "-1234").value is True
        assert numeric_match("-1 234", "-1234").value is True
        assert numeric_match("-42", "42").value is False

    def test_non_numeric_strings(self):
        """Test behavior with non-numeric strings."""
        assert numeric_match("abc", "123").value is False
        assert numeric_match("123", "abc").value is False
        assert numeric_match("abc", "abc").value is False
        assert numeric_match("12a3", "123").value is False

    def test_special_values(self):
        """Test special values."""
        assert numeric_match("inf", "inf").value is True
        assert numeric_match("-inf", "-inf").value is True
        assert numeric_match("nan", "nan").value is False  # NaN != NaN
        assert numeric_match(float("inf"), float("inf")).value is True

    def test_none_values(self):
        """Test None values."""
        assert numeric_match(None, None).value is False
        assert numeric_match(None, 42).value is False
        assert numeric_match(42, None).value is False

    def test_empty_strings(self):
        """Test empty strings."""
        assert numeric_match("", "").value is False
        assert numeric_match("", "0").value is False
        assert numeric_match("0", "").value is False

    def test_mixed_formats(self):
        """Test mixed number formats."""
        assert numeric_match("1.234e3", "1,234").value is True
        assert numeric_match("1,234.00", "1.234e3").value is True
        assert numeric_match("042", "4.2e1").value is True
        assert numeric_match(" 1,234.50 ", "1234.5").value is True
        assert numeric_match("1 234.50", "1,234.5").value is True

    def test_very_large_numbers(self):
        """Test very large numbers."""
        assert numeric_match("1e100", "1e100").value is True
        assert (
            numeric_match(
                "123456789012345678901234567890", "123456789012345678901234567890"
            ).value
            is True
        )

    def test_very_small_numbers(self):
        """Test very small numbers."""
        assert numeric_match("1e-100", "1e-100").value is True
        assert numeric_match("0.0000000001", "1e-10").value is True

    def test_metadata_capture(self):
        """Test that metadata is properly captured."""
        score = numeric_match("42", "42")
        assert score.metadata["result"] == "42"
        assert score.metadata["expected"] == "42"

    def test_decimal_precision_edge_cases(self):
        """Test decimal precision edge cases."""
        # These should be equal when parsed as floats
        assert numeric_match("0.1", "0.10").value is True
        assert numeric_match("1.0", "1").value is True

        # Test known floating point precision issues
        # When parsing from strings, they should be equal
        assert numeric_match("0.3", "0.3").value is True

    def test_edge_cases_with_spaces(self):
        """Test edge cases with space separators."""
        # Space after negative sign
        assert (
            numeric_match("- 1 234", "-1234").value is False
        )  # Space after minus should fail
        assert numeric_match("-1 234", "-1234").value is True  # This should work
        # Mixed separators
        assert numeric_match("1 234,567", "1234567").value is True
        assert numeric_match("1,234 567", "1234567").value is True
