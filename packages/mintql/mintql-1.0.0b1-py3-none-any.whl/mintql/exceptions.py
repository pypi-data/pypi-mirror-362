"""
Exception classes for MintQL.

Provides a hierarchy of exceptions for different types of errors
that can occur during query building and validation.
"""


class MintqlError(Exception):
    """Base exception class for all MintQL errors."""
    pass


class QueryError(MintqlError):
    """Raised when there's an error in query construction or validation."""
    pass


class DialectError(MintqlError):
    """Raised when there's an error related to SQL dialect configuration."""
    pass


class ValidationError(MintqlError):
    """Raised when query validation fails."""
    pass


class UnsupportedOperationError(MintqlError):
    """Raised when an operation is not supported by the current dialect."""
    pass
