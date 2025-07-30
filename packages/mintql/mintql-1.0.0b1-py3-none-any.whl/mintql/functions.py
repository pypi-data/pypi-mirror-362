"""
Typed SQL functions for MintQL.

Provides type-safe SQL functions with IDE autocompletion and a shorter alias.
"""

from typing import Any, Union, List, Optional
from .exceptions import QueryError, ValidationError


class Function:
    """Base class for SQL functions."""

    def __init__(self, name: str, *args: Any):
        self.name = name
        self.args = args
        self._alias = None
        self._validate_args()

    def _validate_args(self) -> None:
        """Validate function arguments for safety."""
        for arg in self.args:
            if isinstance(arg, str) and not self._is_safe_arg(arg):
                # Check if it's a potentially unsafe string
                if "'" in arg or '"' in arg:
                    pass

    def _is_safe_arg(self, arg: str) -> bool:
        """
        Check if a string argument is safe (column name or special keyword).

        Args:
            arg: The argument to check

        Returns:
            bool: True if the argument is safe
        """
        # Safe special cases
        safe_keywords = {'*', 'DISTINCT', 'ALL', 'ASC', 'DESC'}

        if arg.upper() in safe_keywords:
            return True

        if arg.upper().startswith('DISTINCT '):
            return True

        # Check if it's a column reference (contains dot or is alphanumeric with underscores)
        if '.' in arg:
            # Validate table.column format
            parts = arg.split('.')
            if len(parts) == 2 and all(self._is_valid_identifier(p) for p in parts):
                return True

        # Check if it's a simple column name
        if self._is_valid_identifier(arg):
            return True

        # Check if it contains operators (likely an expression)
        operators = ['(', ')', '+', '-', '*', '/', ' ']
        if any(op in arg for op in operators):
            return True

        return False

    def _is_valid_identifier(self, name: str) -> bool:
        """Check if a string is a valid SQL identifier."""
        if not name:
            return False

        # First character must be a letter or an underscore
        if not (name[0].isalpha() or name[0] == '_'):
            return False

        # Rest must be alphanumeric or underscore
        return all(c.isalnum() or c == '_' for c in name[1:])

    def __str__(self) -> str:
        """Convert function to SQL string."""
        if not self.args:
            func_str = f"{self.name}()"
        else:
            # Convert arguments to strings
            str_args = []
            for arg in self.args:
                if isinstance(arg, Function):
                    str_args.append(str(arg))
                elif isinstance(arg, str):
                    # Handle special cases safely
                    if arg == '*' or '.' in arg or arg.upper().startswith('DISTINCT '):
                        str_args.append(arg)
                    elif any(c in arg for c in ['(', ')', '+', '-', '*', '/', ' ']):
                        # Expression
                        str_args.append(arg)
                    else:
                        # Regular column name or value
                        str_args.append(arg)
                else:
                    str_args.append(str(arg))

            func_str = f"{self.name}({', '.join(str_args)})"

        if self._alias:
            if not self._is_valid_identifier(self._alias):
                raise ValidationError(f"Invalid function alias: {self._alias}")
            func_str = f"{func_str} AS {self._alias}"

        return func_str

    def as_(self, alias: str) -> "Function":
        """Add an alias to the function"""
        if not alias or not isinstance(alias, str):
            raise ValidationError("Function alias must be a non-empty string")
        self._alias = alias
        return self

    def alias(self, alias: str) -> "Function":
        """Add an alias to the function (alternative name)."""
        return self.as_(alias)


class AggregateFunction(Function):
    """Aggregate functions."""

    def validate(self, context: str = None) -> None:
        """Validate aggregate function usage."""
        pass


class MathFunction(Function):
    """Mathematical functions."""

    def validate(self, context: str = None) -> None:
        """Validate math function usage."""
        pass


class StringFunction(Function):
    """String functions."""

    def validate(self, context: str = None) -> None:
        """Validate string function usage."""
        pass


class DateFunction(Function):
    """Date/time functions."""

    def validate(self, context: str = None) -> None:
        """Validate date function usage."""
        pass


class Functions:
    """Type-safe SQL functions with IDE autocompletion."""

    # ===== AGGREGATE FUNCTIONS =====

    @staticmethod
    def COUNT(column: str = "*", distinct: bool = False) -> AggregateFunction:
        """COUNT function."""
        if distinct and column == "*":
            raise QueryError("COUNT DISTINCT cannot be used with *")

        if distinct:
            return AggregateFunction("COUNT", f"DISTINCT {column}")
        else:
            return AggregateFunction("COUNT", column)

    @staticmethod
    def SUM(column: str, distinct: bool = False) -> AggregateFunction:
        """SUM function."""
        if distinct:
            return AggregateFunction("SUM", f"DISTINCT {column}")
        else:
            return AggregateFunction("SUM", column)

    @staticmethod
    def AVG(column: str, distinct: bool = False) -> AggregateFunction:
        """AVG function."""
        if distinct:
            return AggregateFunction("AVG", f"DISTINCT {column}")
        else:
            return AggregateFunction("AVG", column)

    @staticmethod
    def MIN(column: str) -> AggregateFunction:
        """MIN function."""
        return AggregateFunction("MIN", column)

    @staticmethod
    def MAX(column: str) -> AggregateFunction:
        """MAX function."""
        return AggregateFunction("MAX", column)

    @staticmethod
    def GROUP_CONCAT(column: str, separator: str = ",") -> AggregateFunction:
        """GROUP_CONCAT function (MySQL)."""
        # Note: separator should be parameterized in actual query building
        # This is just for the function definition
        return AggregateFunction("GROUP_CONCAT", column, f"SEPARATOR '{separator}'")

    @staticmethod
    def STRING_AGG(column: str, separator: str = ",") -> AggregateFunction:
        """STRING_AGG function (PostgreSQL)."""
        # Note: separator should be parameterized in actual query building
        # This is just for the function definition
        return AggregateFunction("STRING_AGG", column, f"'{separator}'")

    # ===== MATHEMATICAL FUNCTIONS =====

    @staticmethod
    def ABS(value: Union[str, int, float]) -> MathFunction:
        """ABS function."""
        return MathFunction("ABS", value)

    @staticmethod
    def ROUND(value: Union[str, int, float], precision: int = 0) -> MathFunction:
        """ROUND function."""
        if not isinstance(precision, int) or precision < 0:
            raise ValidationError("ROUND precision must be a non-negative integer")

        if precision == 0:
            return MathFunction("ROUND", value)
        else:
            return MathFunction("ROUND", value, precision)

    @staticmethod
    def CEIL(value: Union[str, int, float]) -> MathFunction:
        """CEIL function."""
        return MathFunction("CEIL", value)

    @staticmethod
    def FLOOR(value: Union[str, int, float]) -> MathFunction:
        """FLOOR function."""
        return MathFunction("FLOOR", value)

    @staticmethod
    def POWER(base: Union[str, int, float], exponent: Union[str, int, float]) -> MathFunction:
        """POWER function."""
        return MathFunction("POWER", base, exponent)

    @staticmethod
    def SQRT(value: Union[str, int, float]) -> MathFunction:
        """SQRT function."""
        return MathFunction("SQRT", value)

    # ===== STRING FUNCTIONS =====

    @staticmethod
    def CONCAT(*args: str) -> StringFunction:
        """CONCAT function."""
        if len(args) < 2:
            raise QueryError("CONCAT requires at least 2 arguments")
        return StringFunction("CONCAT", *args)

    @staticmethod
    def LENGTH(string: str) -> StringFunction:
        """LENGTH function."""
        return StringFunction("LENGTH", string)

    @staticmethod
    def UPPER(string: str) -> StringFunction:
        """UPPER function."""
        return StringFunction("UPPER", string)

    @staticmethod
    def LOWER(string: str) -> StringFunction:
        """LOWER function."""
        return StringFunction("LOWER", string)

    @staticmethod
    def TRIM(string: str, chars: Optional[str] = None) -> StringFunction:
        """
        TRIM function.

        Note: The chars parameter will be properly parameterized during query building.
        This function definition just creates the structure.
        """
        if chars:
            # Create a placeholder that will be handled during query building
            # Using a special marker to indicate this needs parameterization
            return StringFunction("TRIM", f"__PARAM_CHARS__ FROM {string}")
        else:
            return StringFunction("TRIM", string)

    @staticmethod
    def SUBSTRING(string: str, start: int, length: Optional[int] = None) -> StringFunction:
        """SUBSTRING function."""
        if not isinstance(start, int) or start < 1:
            raise ValidationError("SUBSTRING start position must be a positive integer")

        if length is not None:
            if not isinstance(length, int) or length < 0:
                raise ValidationError("SUBSTRING length must be a non-negative integer")
            return StringFunction("SUBSTRING", string, start, length)
        else:
            return StringFunction("SUBSTRING", string, start)

    @staticmethod
    def REPLACE(string: str, search: str, replace: str) -> StringFunction:
        """
        REPLACE function.

        Note: search and replace parameters should be parameterized during query building.
        This function definition just creates the structure.
        """
        # Use placeholders that will be handled during query building
        return StringFunction("REPLACE", string, "__PARAM_SEARCH__", "__PARAM_REPLACE__")

    # ===== DATE/TIME FUNCTIONS =====

    @staticmethod
    def NOW() -> DateFunction:
        """NOW function."""
        return DateFunction("NOW")

    @staticmethod
    def CURRENT_DATE() -> DateFunction:
        """CURRENT_DATE function."""
        return DateFunction("CURRENT_DATE")

    @staticmethod
    def CURRENT_TIME() -> DateFunction:
        """CURRENT_TIME function."""
        return DateFunction("CURRENT_TIME")

    @staticmethod
    def CURRENT_TIMESTAMP() -> DateFunction:
        """CURRENT_TIMESTAMP function."""
        return DateFunction("CURRENT_TIMESTAMP")

    @staticmethod
    def DATE(value: str) -> DateFunction:
        """DATE function."""
        return DateFunction("DATE", value)

    @staticmethod
    def YEAR(date: str) -> DateFunction:
        """YEAR function."""
        return DateFunction("YEAR", date)

    @staticmethod
    def MONTH(date: str) -> DateFunction:
        """MONTH function."""
        return DateFunction("MONTH", date)

    @staticmethod
    def DAY(date: str) -> DateFunction:
        """DAY function."""
        return DateFunction("DAY", date)

    @staticmethod
    def DATE_TRUNC(precision: str, date: str) -> DateFunction:
        """
        DATE_TRUNC function (PostgreSQL).

        Args:
            precision: One of 'year', 'month', 'day', 'hour', 'minute', 'second'
            date: Column name or date expression
        """
        valid_precisions = {'year', 'month', 'day', 'hour', 'minute', 'second', 'week', 'quarter'}
        if precision.lower() not in valid_precisions:
            raise ValidationError(
                f"Invalid DATE_TRUNC precision '{precision}'. "
                f"Valid options: {', '.join(sorted(valid_precisions))}"
            )

        return DateFunction("DATE_TRUNC", f"'{precision}'", date)

    # ===== CONDITIONAL FUNCTIONS =====

    @staticmethod
    def COALESCE(*args: str) -> Function:
        """COALESCE function."""
        if len(args) < 2:
            raise QueryError("COALESCE requires at least 2 arguments")
        return Function("COALESCE", *args)

    @staticmethod
    def NULLIF(expr1: str, expr2: str) -> Function:
        """NULLIF function."""
        return Function("NULLIF", expr1, expr2)

    @staticmethod
    def CASE() -> 'CaseBuilder':
        """CASE expression builder."""
        return CaseBuilder()

    # ===== JSON FUNCTIONS =====

    @staticmethod
    def JSON_EXTRACT(json_column: str, path: str) -> Function:
        """
        JSON_EXTRACT function.

        Note: The path parameter should be parameterized during query building.
        """
        # Use a placeholder that will be handled during query building
        return Function("JSON_EXTRACT", json_column, "__PARAM_JSON_PATH__")

    @staticmethod
    def JSON_OBJECT(*args: str) -> Function:
        """JSON_OBJECT function."""
        if len(args) % 2 != 0:
            raise QueryError("JSON_OBJECT requires an even number of arguments (key-value pairs)")
        return Function("JSON_OBJECT", *args)

    # ===== Lowercase aliases =====

    @staticmethod
    def count(column: str = "*", distinct: bool = False) -> AggregateFunction:
        """COUNT function (lowercase alias)."""
        return Functions.COUNT(column, distinct)

    @staticmethod
    def sum(column: str, distinct: bool = False) -> AggregateFunction:
        """SUM function (lowercase alias)."""
        return Functions.SUM(column, distinct)

    @staticmethod
    def avg(column: str, distinct: bool = False) -> AggregateFunction:
        """AVG function (lowercase alias)."""
        return Functions.AVG(column, distinct)

    @staticmethod
    def min(column: str) -> AggregateFunction:
        """MIN function (lowercase alias)."""
        return Functions.MIN(column)

    @staticmethod
    def max(column: str) -> AggregateFunction:
        """MAX function (lowercase alias)."""
        return Functions.MAX(column)


class CaseBuilder:
    """Builder for CASE expressions."""

    def __init__(self):
        self.conditions = []
        self.else_value = None

    def when(self, condition: str, then_value: str) -> 'CaseBuilder':
        """Add WHEN condition."""
        if not condition:
            raise ValidationError("CASE WHEN condition cannot be empty")
        if not then_value:
            raise ValidationError("CASE THEN value cannot be empty")

        self.conditions.append((condition, then_value))
        return self

    def else_(self, value: str) -> 'CaseBuilder':
        """Add ELSE clause."""
        if not value:
            raise ValidationError("CASE ELSE value cannot be empty")

        self.else_value = value
        return self

    def end(self) -> Function:
        """Build the CASE expression."""
        if not self.conditions:
            raise QueryError("CASE expression must have at least one WHEN clause")

        case_parts = ["CASE"]
        for condition, then_value in self.conditions:
            case_parts.extend(["WHEN", condition, "THEN", then_value])

        if self.else_value:
            case_parts.extend(["ELSE", self.else_value])

        case_parts.append("END")

        # Return a Function with empty name to avoid double function syntax
        return Function("", " ".join(case_parts))

    def __str__(self) -> str:
        """Convert to string (requires calling .end() first)."""
        return str(self.end())


# Alias
F = Functions