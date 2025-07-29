import inspect
import json
from typing import Any, Optional

from doteval.metrics import Metric, accuracy
from doteval.models import Score


def evaluator(metrics: Metric | list[Metric]):
    if not isinstance(metrics, list):
        metrics = [metrics]

    def decorator(func):
        def wrapper(*args, **kwargs):
            # Extract custom name from kwargs if provided
            custom_name = kwargs.pop("name", None)
            value = func(*args, **kwargs)
            metadata = get_metadata(func, *args, **kwargs)

            # Use custom name if provided, otherwise use function name
            score_name = custom_name if custom_name is not None else func.__name__
            return Score(score_name, value, metrics, metadata)

        wrapper.__name__ = func.__name__

        return wrapper

    return decorator


def get_metadata(func, *args, **kwargs):
    sig = inspect.signature(func)
    param_names = list(sig.parameters.keys())

    metadata = {}
    for i, arg in enumerate(args):
        if i < len(param_names):
            metadata[param_names[i]] = arg

    metadata.update(kwargs)

    return metadata


@evaluator(metrics=accuracy())
def exact_match(result, expected, name: Optional[str] = None) -> bool:
    return result == expected


@evaluator(metrics=accuracy())
def numeric_match(result, expected, name: Optional[str] = None) -> bool:
    """Compare numeric values, handling various formats like commas, spaces, and scientific notation.

    Examples:
        numeric_match("1234", "1,234") -> True
        numeric_match("1234", "1 234") -> True
        numeric_match("1234", "1.234e3") -> True
        numeric_match("42", 42) -> True
        numeric_match("3.14", 3.14) -> True
        numeric_match("1,234.56", "1234.56") -> True
        numeric_match("1 234 567", "1234567") -> True
        numeric_match("-1,234", "-1234") -> True
        numeric_match("0.50", "0.5") -> True
        numeric_match(" 42 ", "42") -> True
        numeric_match("nan", "nan") -> False
        numeric_match("abc", "123") -> False
    """
    # Handle None and empty values
    if result is None or expected is None:
        return False

    # Convert to strings for processing
    value_str = str(result).strip()
    expected_str = str(expected).strip()

    # Handle empty strings
    if not value_str or not expected_str:
        return False

    # Try to parse as numbers
    try:
        # Remove thousand separators (commas and spaces)
        # But preserve the space after a minus sign as that's invalid
        def clean_number(s):
            # Check if there's a space after minus sign at the beginning
            if s.startswith("- "):
                # This is invalid, return as-is to let float() fail
                return s
            # Otherwise remove commas and spaces
            return s.replace(",", "").replace(" ", "")

        value_clean = clean_number(value_str)
        expected_clean = clean_number(expected_str)

        # Parse to float
        value_num = float(value_clean)
        expected_num = float(expected_clean)

        # Handle NaN case (NaN != NaN in Python)
        if value_clean.lower() == "nan" and expected_clean.lower() == "nan":
            return False

        # Compare the numeric values
        return value_num == expected_num
    except (ValueError, AttributeError):
        # If parsing fails, values are not numeric
        return False


@evaluator(metrics=accuracy())
def valid_json(result: Any, schema: Optional[dict] = None) -> bool:
    """Check if a value is valid JSON and optionally validate against a JSON schema.

    Args:
        result: The value to check - typically a string containing JSON
        schema: Optional JSON schema dict to validate against

    Examples:
        valid_json('{"name": "John"}') -> True
        valid_json('{"name": "John",}') -> False (trailing comma)
        valid_json('["a", "b", "c"]') -> True
        valid_json('123') -> True (valid JSON number)
        valid_json('invalid') -> False

        # With schema validation
        schema = {"type": "object", "required": ["name"]}
        valid_json('{"name": "John"}', schema) -> True
        valid_json('{"age": 30}', schema) -> False (missing required field)

    Returns:
        True if value is valid JSON (and matches schema if provided), False otherwise
    """
    # Handle None and empty values
    if result is None:
        return False

    # Convert to string
    value_str = str(result).strip()

    # Handle empty strings
    if not value_str:
        return False

    try:
        # Try to parse the JSON
        parsed = json.loads(value_str)

        # If no schema provided, just check if it's valid JSON
        if schema is None:
            return True

        # If schema provided, validate against it using jsonschema
        import jsonschema

        jsonschema.validate(instance=parsed, schema=schema)
        return True

    except (json.JSONDecodeError, ValueError):
        # If parsing fails, it's not valid JSON
        return False
    except jsonschema.ValidationError:
        # JSON is valid but doesn't match schema
        return False
    except jsonschema.SchemaError:
        # The schema itself is invalid
        return False
