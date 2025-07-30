"""
Typed operators for MintQL.

Provides type-safe operators with both enum-style and string support.
"""

from typing import Any, Union, Protocol
from .exceptions import QueryError


class Operator(Protocol):
    """Protocol for operators."""
    value: str

    def validate(self, column: str, value: Any) -> None:
        ...


class ComparisonOperator:
    """Comparison operators."""
    def __init__(self, value: str):
        self.value = value

    def validate(self, column: str, value: Any) -> None:
        """Basic validation for comparison operators."""
        pass

    def __str__(self) -> str:
        return self.value


class NullOperator:
    """Operators for NULL comparisons."""
    def __init__(self, value: str):
        self.value = value

    def validate(self, column: str, value: Any) -> None:
        """Validate NULL operators."""
        if value is not None:
            raise QueryError(f"Operator {self.value} should be used with None/NULL value")

    def __str__(self) -> str:
        return self.value


class ListOperator:
    """Operators for list operations."""
    def __init__(self, value: str):
        self.value = value

    def validate(self, column: str, value: Any) -> None:
        """Validate list operators."""
        if not isinstance(value, (list, tuple)):
            raise QueryError(f"Operator {self.value} requires a list or tuple value")

    def __str__(self) -> str:
        return self.value


class PatternOperator:
    """Operators for pattern matching."""
    def __init__(self, value: str):
        self.value = value

    def validate(self, column: str, value: Any) -> None:
        """Validate pattern operators."""
        if not isinstance(value, str):
            raise QueryError(f"Operator {self.value} requires a string pattern")

    def __str__(self) -> str:
        return self.value


class RangeOperator:
    """Operators for range operations."""
    def __init__(self, value: str):
        self.value = value

    def validate(self, column: str, value: Any) -> None:
        """Validate range operators."""
        if not isinstance(value, (list, tuple)) or len(value) != 2:
            raise QueryError(f"Operator {self.value} requires a list/tuple with exactly 2 values")

    def __str__(self) -> str:
        return self.value


class JsonOperator:
    """Operators for JSON operations."""
    def __init__(self, value: str):
        self.value = value

    def validate(self, column: str, value: Any) -> None:
        """Validate JSON operators."""
        pass  # JSON validation depends on dialect

    def __str__(self) -> str:
        return self.value


class Operators:
    """Type-safe SQL operators with IDE autocompletion."""

    # Comparison
    EQUALS = ComparisonOperator("=")
    EQ = EQUALS  # Alias
    NOT_EQUALS = ComparisonOperator("!=")
    NE = NOT_EQUALS  # Alias
    NOT_EQUALS_ALT = ComparisonOperator("<>")
    LESS_THAN = ComparisonOperator("<")
    LT = LESS_THAN  # Alias
    LESS_THAN_OR_EQUAL = ComparisonOperator("<=")
    LTE = LESS_THAN_OR_EQUAL  # Alias
    GREATER_THAN = ComparisonOperator(">")
    GT = GREATER_THAN  # Alias
    GREATER_THAN_OR_EQUAL = ComparisonOperator(">=")
    GTE = GREATER_THAN_OR_EQUAL  # Alias

    # NULL
    IS = NullOperator("IS")
    IS_NOT = NullOperator("IS NOT")

    # List
    IN = ListOperator("IN")
    NOT_IN = ListOperator("NOT IN")

    # Pattern matching
    LIKE = PatternOperator("LIKE")
    NOT_LIKE = PatternOperator("NOT LIKE")
    ILIKE = PatternOperator("ILIKE")  # Case-insensitive (PostgreSQL specific)
    NOT_ILIKE = PatternOperator("NOT ILIKE")

    # Range
    BETWEEN = RangeOperator("BETWEEN")
    NOT_BETWEEN = RangeOperator("NOT BETWEEN")

    # Advanced
    REGEX = PatternOperator("REGEX")  # Translated to dialect-specific operator
    NOT_REGEX = PatternOperator("NOT REGEX")
    JSON_CONTAINS = JsonOperator("JSON_CONTAINS")
    JSON_EXISTS = JsonOperator("JSON_EXISTS")

    @classmethod
    def from_string(cls, value: str) -> Union[ComparisonOperator, NullOperator, ListOperator, PatternOperator, RangeOperator, JsonOperator]:
        """Convert string to operator for backward compatibility and string operator support."""

        original_value = value
        value = value.upper()

        # Direct string operators
        simple_operators = {
            "=": cls.EQUALS,
            "==": cls.EQUALS,
            "!=": cls.NOT_EQUALS,
            "<>": cls.NOT_EQUALS_ALT,
            "<": cls.LESS_THAN,
            "<=": cls.LESS_THAN_OR_EQUAL,
            ">": cls.GREATER_THAN,
            ">=": cls.GREATER_THAN_OR_EQUAL,
        }

        # Check simple operators first
        if original_value in simple_operators:
            return simple_operators[original_value]

        # Map of string values to operators (uppercase)
        operator_map = {
            "=": cls.EQUALS,
            "==": cls.EQUALS,
            "!=": cls.NOT_EQUALS,
            "<>": cls.NOT_EQUALS_ALT,
            "<": cls.LESS_THAN,
            "<=": cls.LESS_THAN_OR_EQUAL,
            ">": cls.GREATER_THAN,
            ">=": cls.GREATER_THAN_OR_EQUAL,
            "IS": cls.IS,
            "IS NOT": cls.IS_NOT,
            "IN": cls.IN,
            "NOT IN": cls.NOT_IN,
            "LIKE": cls.LIKE,
            "NOT LIKE": cls.NOT_LIKE,
            "ILIKE": cls.ILIKE,
            "NOT ILIKE": cls.NOT_ILIKE,
            "BETWEEN": cls.BETWEEN,
            "NOT BETWEEN": cls.NOT_BETWEEN,
            "REGEX": cls.REGEX,
            "NOT REGEX": cls.NOT_REGEX,
            "~": cls.REGEX,  # PostgreSQL style
            "!~": cls.NOT_REGEX,  # PostgreSQL style
            "REGEXP": cls.REGEX,  # MySQL style
            "NOT REGEXP": cls.NOT_REGEX,  # MySQL style
            "JSON_CONTAINS": cls.JSON_CONTAINS,
            "JSON_EXISTS": cls.JSON_EXISTS,
        }

        if value in operator_map:
            return operator_map[value]

        # Try with original case for case-sensitive operators
        if original_value in operator_map.values():
            for k, v in operator_map.items():
                if original_value == k:
                    return v

        raise QueryError(
            f"Unknown operator '{original_value}'. "
            f"Available: =, !=, <, >, <=, >=, IN, LIKE, BETWEEN, etc."
        )

# Alias for Operators class
O = Operators