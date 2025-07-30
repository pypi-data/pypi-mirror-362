"""
SQL dialect support for different database systems.

Handles differences in parameter styles, quoting, and SQL syntax.
Currently supported: PostgreSQL, MySQL, and SQLite.
"""

from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict, Union
from .exceptions import DialectError, ValidationError


class Dialects(Enum):
    """Enum for type-safe dialect selection."""
    POSTGRESQL = "postgresql"
    MYSQL = "mysql"
    SQLITE = "sqlite"

    @classmethod
    def from_string(cls, value: str) -> 'Dialects':
        """Convert string to Dialects enum."""
        value = value.lower()

        # Handle common aliases
        aliases = {
            'postgres': 'postgresql',
            'pg': 'postgresql'
        }
        value = aliases.get(value, value)

        for dialect in cls:
            if dialect.value == value:
                return dialect

        available = ", ".join([d.value for d in cls])
        raise DialectError(
            f"Unknown dialect '{value}'. Available: {available}"
        )


class Dialect(ABC):
    """Abstract base class."""

    def __init__(self):
        self.param_style = "pyformat"
        self.quote_char = '"'
        self.escape_char = "\\"
        self.supports_returning = False
        self.supports_on_conflict = False
        self.supports_cte = True
        self.supports_window = True
        self.supports_json_operators = False
        self.supports_regex_operator = False
        self.supports_full_outer_join = True
        self.max_identifier_length = 63  # Default - overridden in subclasses

    @abstractmethod
    def format_param(self, index: int) -> str:
        """Format a parameter placeholder for this dialect."""
        pass

    def validate_identifier(self, name: str) -> None:
        """
        Validate an identifier (table/column name) for safety.

        Args:
            name: The identifier to validate

        Raises:
            ValidationError: If the identifier is invalid
        """
        if not name or not isinstance(name, str):
            raise ValidationError("Identifier must be a non-empty string")

        # Check length
        if len(name) > self.max_identifier_length:
            raise ValidationError(
                f"Identifier '{name}' exceeds maximum length of {self.max_identifier_length} characters"
            )

        # Check for quote characters
        if self.quote_char in name:
            raise ValidationError(
                f"Identifier '{name}' contains quote character '{self.quote_char}' which is not allowed"
            )

        # Check for valid identifier pattern (alphanumeric, underscore, and dollar sign for some dialects)
        # First character must be letter or underscore
        if not name[0].isalpha() and name[0] != '_':
            raise ValidationError(
                f"Identifier '{name}' must start with a letter or underscore"
            )

        # Check the rest of the characters
        for char in name[1:]:
            if not (char.isalnum() or char in ('_', '$')):
                raise ValidationError(
                    f"Identifier '{name}' contains invalid character '{char}'. "
                    f"Only letters, numbers, underscores, and dollar signs are allowed."
                )

    def quote_identifier(self, name: str) -> str:
        """
        Quote an identifier (table/column name) for this dialect.

        Args:
            name: The identifier to quote

        Returns:
            str: The properly quoted identifier

        Raises:
            ValidationError: If the identifier is invalid
        """
        if not name or not isinstance(name, str):
            raise ValidationError("Identifier must be a non-empty string")

        # Do not quote if already quoted
        if name.startswith(self.quote_char) and name.endswith(self.quote_char):
            # Validate inner part
            inner_name = name[1:-1]
            if self.quote_char in inner_name:
                raise ValidationError(
                    f"Already quoted identifier contains quote character '{self.quote_char}'"
                )
            return name

        # Handle table.column notation
        if '.' in name:
            parts = name.split('.', 1)
            for part in parts:
                self.validate_identifier(part)
            return f"{self.quote_identifier(parts[0])}.{self.quote_identifier(parts[1])}"

        self.validate_identifier(name)

        return f"{self.quote_char}{name}{self.quote_char}"

    def format_limit(self, limit: int, offset: int = None) -> str:
        """
        Format LIMIT/OFFSET clause for this dialect.

        Args:
            limit: The limit value
            offset: Optional offset value

        Returns:
            str: Formatted LIMIT/OFFSET clause

        Raises:
            ValidationError: If limit or offset are invalid
        """
        if limit is None:
            return ""

        if not isinstance(limit, int) or limit < 0:
            raise ValidationError("LIMIT must be a non-negative integer")

        if offset is not None and (not isinstance(offset, int) or offset < 0):
            raise ValidationError("OFFSET must be a non-negative integer")

        clause = f"LIMIT {limit}"
        if offset is not None:
            clause += f" OFFSET {offset}"
        return clause

    @abstractmethod
    def format_json_extract(self, column: str, path: str) -> str:
        """Format JSON extraction for this dialect."""
        pass

    @abstractmethod
    def format_regex_match(self, column: str, pattern: str) -> str:
        """Format regex matching for this dialect."""
        pass


class PostgreSQLDialect(Dialect):
    """PostgreSQL dialect."""

    def __init__(self):
        super().__init__()
        self.param_style = "numbered"
        self.quote_char = '"'
        self.supports_returning = True
        self.supports_on_conflict = True
        self.supports_cte = True
        self.supports_window = True
        self.supports_json_operators = True
        self.supports_regex_operator = True
        self.supports_full_outer_join = True
        self.max_identifier_length = 63

    def format_param(self, index: int) -> str:
        """Format parameter as $1, $2, etc."""
        if not isinstance(index, int) or index < 0:
            raise ValidationError("Parameter index must be a non-negative integer")
        return f"${index + 1}"

    def format_json_extract(self, column: str, path: str) -> str:
        """Format JSON extraction using PostgreSQL syntax."""
        # Validate column identifier
        if '.' in column:
            parts = column.split('.', 1)
            for part in parts:
                self.validate_identifier(part)
        else:
            self.validate_identifier(column)

        return f"{column}->>{path}"

    def format_regex_match(self, column: str, pattern: str) -> str:
        """Format regex matching using PostgreSQL syntax."""
        # Validate column identifier
        if '.' in column:
            parts = column.split('.', 1)
            for part in parts:
                self.validate_identifier(part)
        else:
            self.validate_identifier(column)

        return f"{column} ~ {pattern}"


class MySQLDialect(Dialect):
    """MySQL dialect."""

    def __init__(self):
        super().__init__()
        self.param_style = "qmark"
        self.quote_char = "`"
        self.supports_returning = False
        self.supports_on_conflict = False
        self.supports_cte = True
        self.supports_window = True
        self.supports_json_operators = True
        self.supports_regex_operator = True
        self.supports_full_outer_join = False  # MySQL doesn't support FULL OUTER JOIN
        self.max_identifier_length = 64

    def format_param(self, index: int) -> str:
        """Format parameter as ?."""
        if not isinstance(index, int) or index < 0:
            raise ValidationError("Parameter index must be a non-negative integer")
        return "?"

    def format_json_extract(self, column: str, path: str) -> str:
        """Format JSON extraction using MySQL syntax."""
        # Validate column identifier
        if '.' in column:
            parts = column.split('.', 1)
            for part in parts:
                self.validate_identifier(part)
        else:
            self.validate_identifier(column)

        return f"JSON_EXTRACT({column}, {path})"

    def format_regex_match(self, column: str, pattern: str) -> str:
        """Format regex matching using MySQL syntax."""
        # Validate column identifier
        if '.' in column:
            parts = column.split('.', 1)
            for part in parts:
                self.validate_identifier(part)
        else:
            self.validate_identifier(column)

        return f"{column} REGEXP {pattern}"


class SQLiteDialect(Dialect):
    """SQLite dialect."""

    def __init__(self):
        super().__init__()
        self.param_style = "qmark"
        self.quote_char = '"'
        self.supports_returning = False
        self.supports_on_conflict = True
        self.supports_cte = True
        self.supports_window = True
        self.supports_json_operators = True
        self.supports_regex_operator = False  # Not built-in
        self.supports_full_outer_join = False  # SQLite doesn't support FULL OUTER JOIN
        self.max_identifier_length = 255

    def format_param(self, index: int) -> str:
        """Format parameter as ?."""
        if not isinstance(index, int) or index < 0:
            raise ValidationError("Parameter index must be a non-negative integer")
        return "?"

    def format_json_extract(self, column: str, path: str) -> str:
        """Format JSON extraction using SQLite syntax."""
        # Validate column identifier
        if '.' in column:
            parts = column.split('.', 1)
            for part in parts:
                self.validate_identifier(part)
        else:
            self.validate_identifier(column)

        return f"JSON_EXTRACT({column}, {path})"

    def format_regex_match(self, column: str, pattern: str) -> str:
        raise DialectError("SQLite does not support regex matching natively. Consider using LIKE instead.")


# Available dialects
DIALECTS: Dict[str, Dialect] = {
    "postgresql": PostgreSQLDialect(),
    "postgres": PostgreSQLDialect(),
    "pg": PostgreSQLDialect(),
    "mysql": MySQLDialect(),
    "sqlite": SQLiteDialect(),
}


def get_dialect(name: Union[str, Dialects]) -> Dialect:
    """
    Get a dialect by name or enum.

    Args:
        name: Dialect name or enum value

    Returns:
        Dialect: The requested dialect instance

    Raises:
        DialectError: If the dialect is unknown
    """
    if isinstance(name, Dialects):
        name = name.value

    name_lower = name.lower() if isinstance(name, str) else name

    if name_lower not in DIALECTS:
        available = ", ".join(DIALECTS.keys())
        raise DialectError(
            f"Unknown dialect '{name}'. Available: {available}"
        )
    return DIALECTS[name_lower]