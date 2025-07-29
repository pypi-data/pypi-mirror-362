"""Tests for the valid_json evaluator."""

from doteval.evaluators import valid_json
from doteval.models import Score


class TestValidJson:
    """Test cases for valid_json evaluator."""

    def test_valid_json_object(self):
        """Test valid JSON object."""
        score = valid_json('{"name": "John", "age": 30}')
        assert isinstance(score, Score)
        assert score.value is True
        assert score.name == "valid_json"

    def test_valid_json_array(self):
        """Test valid JSON array."""
        assert valid_json('["apple", "banana", "cherry"]').value is True
        assert valid_json("[1, 2, 3, 4, 5]").value is True

    def test_valid_json_primitives(self):
        """Test valid JSON primitives."""
        assert valid_json('"hello"').value is True
        assert valid_json("123").value is True
        assert valid_json("123.45").value is True
        assert valid_json("true").value is True
        assert valid_json("false").value is True
        assert valid_json("null").value is True

    def test_valid_nested_json(self):
        """Test valid nested JSON."""
        json_str = """
        {
            "users": [
                {"name": "Alice", "age": 25},
                {"name": "Bob", "age": 30}
            ],
            "total": 2
        }
        """
        assert valid_json(json_str).value is True

    def test_invalid_json_syntax(self):
        """Test invalid JSON syntax."""
        assert valid_json('{name: "John"}').value is False  # Missing quotes
        assert valid_json('{"name": "John",}').value is False  # Trailing comma
        assert valid_json("{'name': 'John'}").value is False  # Single quotes
        assert valid_json("{").value is False  # Incomplete
        assert valid_json("undefined").value is False  # Not valid JSON

    def test_empty_and_none_values(self):
        """Test empty and None values."""
        assert valid_json("").value is False
        assert valid_json(None).value is False

    def test_whitespace_handling(self):
        """Test whitespace handling."""
        assert valid_json('  {"name": "John"}  ').value is True
        assert valid_json('\n{\n"name":\n"John"\n}\n').value is True

    def test_json_with_schema_valid(self):
        """Test JSON validation against schema - valid cases."""
        schema = {
            "type": "object",
            "properties": {"name": {"type": "string"}, "age": {"type": "number"}},
            "required": ["name", "age"],
        }

        json_str = '{"name": "John", "age": 30}'
        assert valid_json(json_str, schema).value is True

        # With additional properties
        json_str = '{"name": "John", "age": 30, "city": "NYC"}'
        assert valid_json(json_str, schema).value is True

    def test_json_with_schema_invalid(self):
        """Test JSON validation against schema - invalid cases."""
        schema = {
            "type": "object",
            "properties": {"name": {"type": "string"}, "age": {"type": "number"}},
            "required": ["name", "age"],
        }

        # Missing required field
        assert valid_json('{"name": "John"}', schema).value is False

        # Wrong type
        assert valid_json('{"name": "John", "age": "thirty"}', schema).value is False

        # Valid JSON but doesn't match schema
        assert valid_json('["array", "instead", "of", "object"]', schema).value is False

    def test_complex_schema_validation(self):
        """Test complex schema validation."""
        schema = {
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
                "code": {"type": "string", "minLength": 3, "maxLength": 10},
                "items": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "price": {"type": "number", "minimum": 0},
                        },
                    },
                },
            },
        }

        valid_data = """
        {
            "id": 123,
            "code": "ABC123",
            "items": [
                {"name": "Apple", "price": 1.99},
                {"name": "Banana", "price": 0.99}
            ]
        }
        """
        assert valid_json(valid_data, schema).value is True

        # Invalid - code too short
        invalid_data = """
        {
            "id": 123,
            "code": "AB",
            "items": []
        }
        """
        assert valid_json(invalid_data, schema).value is False

    def test_invalid_json_with_schema(self):
        """Test that invalid JSON fails even with schema."""
        schema = {"type": "object"}
        assert valid_json("{invalid json}", schema).value is False

    def test_metadata_capture(self):
        """Test that metadata is properly captured."""
        score = valid_json('{"test": true}')
        assert score.metadata["result"] == '{"test": true}'
        assert "schema" not in score.metadata

        schema = {"type": "object"}
        score = valid_json('{"test": true}', schema)
        assert score.metadata["result"] == '{"test": true}'
        assert score.metadata["schema"] == schema

    def test_non_string_input(self):
        """Test behavior with non-string inputs."""
        # Should convert to string and try to parse
        assert valid_json(123).value is True  # Valid JSON number
        assert (
            valid_json({"already": "dict"}).value is False
        )  # Can't parse Python dict as JSON string

    def test_unicode_handling(self):
        """Test Unicode in JSON."""
        assert valid_json('{"name": "José", "city": "São Paulo"}').value is True
        assert valid_json('{"emoji": "🚀"}').value is True

    def test_large_numbers(self):
        """Test large numbers in JSON."""
        assert valid_json('{"value": 9999999999999999999999}').value is True
        assert valid_json('{"value": 1.23e+100}').value is True

    def test_nested_arrays_and_objects(self):
        """Test deeply nested structures."""
        deep_json = """
        {
            "level1": {
                "level2": {
                    "level3": {
                        "array": [
                            [1, 2, 3],
                            [4, 5, 6]
                        ]
                    }
                }
            }
        }
        """
        assert valid_json(deep_json).value is True

    def test_schema_with_pattern(self):
        """Test schema with regex pattern."""
        schema = {
            "type": "object",
            "properties": {
                "phone": {"type": "string", "pattern": "^\\d{3}-\\d{3}-\\d{4}$"}
            },
        }

        assert valid_json('{"phone": "123-456-7890"}', schema).value is True
        assert valid_json('{"phone": "1234567890"}', schema).value is False

    def test_schema_with_enum(self):
        """Test schema with enum constraint."""
        schema = {
            "type": "object",
            "properties": {
                "status": {"type": "string", "enum": ["active", "inactive", "pending"]}
            },
        }

        assert valid_json('{"status": "active"}', schema).value is True
        assert valid_json('{"status": "completed"}', schema).value is False
