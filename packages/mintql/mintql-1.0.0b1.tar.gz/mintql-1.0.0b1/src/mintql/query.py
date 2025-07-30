from typing import List, Dict, Any, Tuple, Union, Optional
from .dialects import Dialect, get_dialect
from .operators import Operators, Operator, ComparisonOperator, NullOperator, ListOperator, PatternOperator, \
    RangeOperator, JsonOperator
from .exceptions import QueryError, ValidationError, MintqlError, UnsupportedOperationError


class ParameterManager:
    """Manages parameter indexing across CTEs and main queries."""

    def __init__(self, dialect: Dialect):
        self.dialect = dialect
        self.params = []
        self.current_offset = 0

    def add_param(self, value: Any) -> str:
        """Add a parameter and return its placeholder."""
        if value is None:
            return "NULL"

        self.params.append(value)
        # Use current offset + position for correct indexing
        index = self.current_offset + len(self.params) - 1
        return self.dialect.format_param(index)

    def get_params(self) -> List[Any]:
        """Get all parameters."""
        return self.params

    def set_offset(self, offset: int) -> None:
        """Set the parameter offset for CTE queries."""
        self.current_offset = offset

    def extend_params(self, params: List[Any]) -> None:
        """Add multiple parameters."""
        self.params.extend(params)


class CTE:
    """Common Table Expression definition."""

    def __init__(self, name: str, query: "SelectQuery", columns: Optional[List[str]] = None, recursive: bool = False):
        """
        Initialize a CTE.

        Args:
            name: Name of the CTE
            query: SelectQuery that defines the CTE
            columns: Optional list of column names
            recursive: Whether this is a recursive CTE
        """
        self.name = name
        self.query = query
        self.columns = columns or []
        self.recursive = recursive

    def to_sql(self, param_manager: ParameterManager) -> str:
        """
        Convert CTE to SQL string using the provided parameter manager.

        Args:
            param_manager: The parameter manager to use for consistent indexing

        Returns:
            str: The CTE SQL definition
        """
        # Set the parameter offset for this CTE
        current_param_count = len(param_manager.get_params())
        self.query._param_manager = param_manager
        self.query._param_manager.set_offset(current_param_count)

        # Handle special recursive CTE query objects
        if hasattr(self.query, '_manual_sql'):
            query_sql = self.query._manual_sql
            # Add the recursive query parameters to the manager
            param_manager.extend_params(self.query._params)
        else:
            # Build the query with the shared parameter manager
            query_sql = self.query._build_sql()

        # Build CTE definition
        cte_sql = self.name
        if self.columns:
            # Validate column names
            for col in self.columns:
                if not col or not isinstance(col, str):
                    raise ValidationError(f"CTE column name must be a non-empty string, got: {col}")
            cte_sql += f" ({', '.join(self.columns)})"
        cte_sql += f" AS ({query_sql})"

        return cte_sql


class Query:
    """Base class for all SQL queries."""

    def __init__(self, dialect: Union[str, Dialect]):
        """
        Initialize query with a dialect.

        Args:
            dialect: Either a dialect name or a Dialect instance
        """
        if dialect is None:
            raise MintqlError("Dialect must be provided")
        elif isinstance(dialect, str):
            self._dialect = get_dialect(dialect)
        else:
            self._dialect = dialect

        self._type = None
        self._param_manager = ParameterManager(self._dialect)
        self._parts = {}
        self._ctes = []

    def with_(self, name: str, query: "SelectQuery", columns: Optional[List[str]] = None) -> "Query":
        """
        Add a CTE (Common Table Expression).

        Args:
            name: Name for the CTE
            query: SelectQuery that defines the CTE
            columns: Optional list of column names for the CTE

        Returns:
            Query: Self for chaining

        Example:
            >>> subquery = mint_pg.select('region', 'SUM(sales) as total').from_('sales').group_by('region')
            >>> query = (mint_pg.select('*').with_('regional_sales', subquery)
            ...           .from_('regional_sales').where('total', '>', 1000))
        """
        if not self._dialect.supports_cte:
            raise UnsupportedOperationError(
                f"Common Table Expressions are not supported in {self._dialect.__class__.__name__}"
            )

        # Validate CTE name
        if not name or not isinstance(name, str):
            raise QueryError("CTE name must be a non-empty string")

        # Additional validation for CTE name
        if not name[0].isalpha() and name[0] != '_':
            raise ValidationError(f"CTE name '{name}' must start with a letter or underscore")

        # Check for duplicate CTE names
        existing_names = [cte.name for cte in self._ctes]
        if name in existing_names:
            raise QueryError(f"CTE name '{name}' already exists")

        cte = CTE(name, query, columns, recursive=False)
        self._ctes.append(cte)
        return self

    def with_recursive(self, name: str, anchor_query: "SelectQuery", recursive_query: "SelectQuery",
                       columns: Optional[List[str]] = None) -> "Query":
        """
        Add a recursive CTE (Common Table Expression).

        Args:
            name: Name for the CTE
            anchor_query: Initial query (non-recursive part)
            recursive_query: Recursive part that references the CTE
            columns: Optional list of column names for the CTE

        Returns:
            Query: Self for chaining

        Example:
            >>> anchor = mint_pg.select('employee_id', 'name', 'manager_id', '0 as level').from_('employees').where('manager_id', 'is', None)
            >>> recursive = mint_pg.select('e.employee_id', 'e.name', 'e.manager_id', 'h.level + 1').from_('employees', 'e').inner_join('hierarchy', 'h', 'e.manager_id', '=', 'h.employee_id')
            >>> query = (mint_pg.select('*').with_recursive('hierarchy', anchor, recursive, ['employee_id', 'name', 'manager_id', 'level'])
            ...           .from_('hierarchy').order_by('level'))
        """
        if not self._dialect.supports_cte:
            raise UnsupportedOperationError(
                f"Common Table Expressions are not supported in {self._dialect.__class__.__name__}"
            )

        # Validate CTE name
        if not name or not isinstance(name, str):
            raise QueryError("CTE name must be a non-empty string")

        # Additional validation for CTE name
        if not name[0].isalpha() and name[0] != '_':
            raise ValidationError(f"CTE name '{name}' must start with a letter or underscore")

        # Check for duplicate CTE names
        existing_names = [cte.name for cte in self._ctes]
        if name in existing_names:
            raise QueryError(f"CTE name '{name}' already exists")

        # Create a special query object for the recursive CTE
        class RecursiveCTEQuery:
            def __init__(self, dialect, anchor_query, recursive_query):
                self._dialect = dialect
                self._anchor_query = anchor_query
                self._recursive_query = recursive_query
                self._param_manager = None

            def _build_sql(self):
                """Build the recursive CTE SQL with proper parameter management."""
                # Use the shared parameter manager if available
                if self._param_manager is not None:
                    # Build anchor query first
                    self._anchor_query._param_manager = self._param_manager
                    anchor_sql = self._anchor_query._build_sql()

                    # Build recursive query with the same parameter manager
                    self._recursive_query._param_manager = self._param_manager
                    recursive_sql = self._recursive_query._build_sql()
                else:
                    # Fallback: build queries independently
                    anchor_sql = self._anchor_query._build_sql()
                    recursive_sql = self._recursive_query._build_sql()

                # Combine with UNION ALL
                return f"{anchor_sql} UNION ALL {recursive_sql}"

        combined_query = RecursiveCTEQuery(self._dialect, anchor_query, recursive_query)
        cte = CTE(name, combined_query, columns, recursive=True)
        self._ctes.append(cte)
        return self

    class CTE:
        """Common Table Expression definition."""

        def __init__(self, name: str, query: "SelectQuery", columns: Optional[List[str]] = None,
                     recursive: bool = False):
            """
            Initialize a CTE.

            Args:
                name: Name of the CTE
                query: SelectQuery that defines the CTE
                columns: Optional list of column names
                recursive: Whether this is a recursive CTE
            """
            self.name = name
            self.query = query
            self.columns = columns or []
            self.recursive = recursive

        def to_sql(self, param_manager: ParameterManager) -> str:
            """
            Convert CTE to SQL string using the provided parameter manager.

            Args:
                param_manager: The parameter manager to use for consistent indexing

            Returns:
                str: The CTE SQL definition
            """
            # Set the parameter manager for this CTE query
            self.query._param_manager = param_manager

            # Build the query SQL
            query_sql = self.query._build_sql()

            # Build CTE definition
            cte_sql = self.name
            if self.columns:
                # Validate column names
                for col in self.columns:
                    if not col or not isinstance(col, str):
                        raise ValidationError(f"CTE column name must be a non-empty string, got: {col}")
                cte_sql += f" ({', '.join(self.columns)})"
            cte_sql += f" AS ({query_sql})"

            return cte_sql

    def _build_cte_clause(self) -> str:
        """Build the WITH clause for CTEs."""
        if not self._ctes:
            return ""

        cte_definitions = []

        # Check if any CTE is recursive
        has_recursive = any(cte.recursive for cte in self._ctes)

        # Use shared parameter manager for all CTEs
        for cte in self._ctes:
            cte_sql = cte.to_sql(self._param_manager)
            cte_definitions.append(cte_sql)

        # Build WITH clause
        with_keyword = "WITH RECURSIVE" if has_recursive else "WITH"
        with_clause = f"{with_keyword} {', '.join(cte_definitions)}"

        return with_clause

    def build(self) -> Tuple[str, List[Any]]:
        """Build the SQL query and return (sql, params) tuple."""
        try:
            if not self._type:
                raise QueryError("Query type not set")

            # Reset parameter manager for fresh build
            self._param_manager = ParameterManager(self._dialect)

            # Build WITH clause first (CTEs)
            with_clause = self._build_cte_clause()

            # Build main query
            main_sql = self._build_sql()

            # Combine WITH clause and main query
            if with_clause:
                sql = f"{with_clause} {main_sql}"
            else:
                sql = main_sql

            return sql.strip(), self._param_manager.get_params()

        except (QueryError, ValidationError, UnsupportedOperationError):
            raise
        except Exception as e:
            raise QueryError(f"Failed to build {self._type} query: {str(e)}") from e

    def _build_sql(self) -> str:
        """Build the SQL string. Overridden in subclasses."""
        raise NotImplementedError("Subclasses must implement _build_sql")

    def _add_param(self, value: Any) -> str:
        """Add a parameter and return its placeholder."""
        return self._param_manager.add_param(value)

    def _normalize_operator(self, operator: Union[str, Operator]) -> Operator:
        """Normalize operator to Operator instance."""
        if isinstance(operator, str):
            return Operators.from_string(operator)
        return operator

    def _check_regex_support(self, operator: Union[str, Operator]) -> None:
        """Check if regex operator is supported by the dialect."""
        # Normalize operator first
        if isinstance(operator, str):
            operator_obj = Operators.from_string(operator)
        else:
            operator_obj = operator

        # Check if it's a regex operator
        if operator_obj.value in ["REGEX", "NOT REGEX"]:
            if not self._dialect.supports_regex_operator:
                raise UnsupportedOperationError(
                    f"Regex matching is not supported in {self._dialect.__class__.__name__}. "
                    f"Consider using LIKE instead."
                )

    def _format_condition(self, column: str, operator: Union[str, Operator], value: Any) -> str:
        """Format a WHERE/HAVING condition."""
        try:
            # Normalize operator
            operator = self._normalize_operator(operator)

            # Validate operator usage
            operator.validate(column, value)

            # Handle NULL values
            if value is None and not isinstance(operator, NullOperator):
                if operator.value == "=":
                    return f"{column} IS NULL"
                elif operator.value in ["!=", "<>"]:
                    return f"{column} IS NOT NULL"

            # Handle special operators
            if operator.value == "BETWEEN":
                if not isinstance(value, (list, tuple)) or len(value) != 2:
                    raise QueryError("BETWEEN requires a list/tuple with exactly 2 values")
                param1 = self._add_param(value[0])
                param2 = self._add_param(value[1])
                return f"{column} BETWEEN {param1} AND {param2}"

            elif operator.value == "NOT BETWEEN":
                if not isinstance(value, (list, tuple)) or len(value) != 2:
                    raise QueryError("NOT BETWEEN requires a list/tuple with exactly 2 values")
                param1 = self._add_param(value[0])
                param2 = self._add_param(value[1])
                return f"{column} NOT BETWEEN {param1} AND {param2}"

            elif operator.value in ["IN", "NOT IN"]:
                if not isinstance(value, (list, tuple)):
                    raise QueryError(f"{operator.value} requires a list or tuple value")

                if not value:
                    # Empty list handling
                    if operator.value == "IN":
                        return "1=0"
                    else:
                        return f"{column} IS NOT NULL"

                placeholders = [self._add_param(v) for v in value]
                return f"{column} {operator.value} ({', '.join(placeholders)})"

            elif operator.value == "REGEX":
                if not self._dialect.supports_regex_operator:
                    raise UnsupportedOperationError(
                        f"Regex matching is not supported in {self._dialect.__class__.__name__}. "
                        f"Consider using LIKE instead."
                    )
                param = self._add_param(value)
                return self._dialect.format_regex_match(column, param)

            elif operator.value == "NOT REGEX":
                if not self._dialect.supports_regex_operator:
                    raise UnsupportedOperationError(
                        f"Regex matching is not supported in {self._dialect.__class__.__name__}. "
                        f"Consider using LIKE instead."
                    )
                param = self._add_param(value)
                return f"NOT ({self._dialect.format_regex_match(column, param)})"

            elif operator.value == "JSON_CONTAINS":
                if not self._dialect.supports_json_operators:
                    raise UnsupportedOperationError(
                        f"JSON operators are not supported in {self._dialect.__class__.__name__}"
                    )
                param = self._add_param(value)
                return f"{self._dialect.format_json_extract(column, param)} IS NOT NULL"

            # Regular condition
            placeholder = self._add_param(value)
            return f"{column} {operator.value} {placeholder}"

        except Exception as e:
            if isinstance(e, (QueryError, ValidationError, UnsupportedOperationError)):
                raise
            raise QueryError(f"Failed to format condition: {str(e)}") from e


class SelectQuery(Query):
    """SELECT query builder with JOIN and CTE support."""

    def __init__(self, dialect: Union[str, Dialect]):
        super().__init__(dialect)
        self._type = "SELECT"
        self._parts = {
            "select": [],
            "from": None,
            "from_alias": None,
            "joins": [],
            "where": [],
            "group_by": [],
            "having": [],
            "order_by": [],
            "limit": None,
            "offset": None,
            "distinct": False
        }

    def select(self, *columns: str) -> "SelectQuery":
        """Add columns to SELECT clause."""
        if not columns:
            self._parts["select"] = ["*"]
        else:
            # Validate column names/expressions
            for col in columns:
                if not col or not isinstance(col, str):
                    raise ValidationError(f"Column must be a non-empty string, got: {col}")
            self._parts["select"].extend(columns)
        return self

    def distinct(self) -> "SelectQuery":
        """Add DISTINCT to SELECT."""
        self._parts["distinct"] = True
        return self

    def from_(self, table: str, alias: str = None) -> "SelectQuery":
        """
        Set the FROM table with optional alias.
        """
        if not table or not isinstance(table, str):
            raise ValidationError("Table name must be a non-empty string")

        # Parse table and alias if provided as single string
        if ' ' in table and alias is None:
            parts = table.split()
            if len(parts) == 2:
                table, alias = parts
            elif len(parts) == 3 and parts[1].upper() == 'AS':
                table, _, alias = parts
            else:
                raise QueryError(f"Invalid table specification: {table}")

        self._parts["from"] = table
        self._parts["from_alias"] = alias
        return self

    def _parse_join_condition(self, condition: str) -> Tuple[str, str, str]:
        """Parse a join condition string like 'table1.col1 = table2.col2'."""
        # Simple parser for common join conditions
        parts = condition.split()
        if len(parts) == 3:
            return parts[0], parts[1], parts[2]
        else:
            raise QueryError(f"Invalid join condition format: {condition}")

    def join(self, table: str, table_alias: str = None, left_column: str = None,
             operator: Union[str, Operator] = None, right_column: str = None,
             join_type: str = "INNER") -> "SelectQuery":
        """
        Add a JOIN clause.

        Can be used in multiple ways:
        - join('orders', 'o', 'users.id', '=', 'o.user_id')
        - join('orders o ON users.id = o.user_id')
        """
        try:
            # Validate join type
            valid_join_types = ["INNER", "LEFT", "RIGHT", "FULL OUTER", "CROSS"]
            if join_type not in valid_join_types:
                raise ValidationError(f"Invalid join type: {join_type}")

            # Parse compact join syntax
            if ' ON ' in table.upper() and left_column is None:
                parts = table.split(' ON ', 1)
                table_part = parts[0].strip()
                condition_part = parts[1].strip()

                # Parse table and alias
                table_parts = table_part.split()
                if len(table_parts) == 2:
                    table, table_alias = table_parts
                elif len(table_parts) == 3 and table_parts[1].upper() == 'AS':
                    table, _, table_alias = table_parts
                else:
                    table = table_parts[0]

                # Parse condition
                left_column, operator, right_column = self._parse_join_condition(condition_part)
                operator = self._normalize_operator(operator)
            else:
                # Traditional syntax - validate inputs
                if not all([left_column, operator, right_column]):
                    raise QueryError("JOIN requires left column, operator, and right column")
                operator = self._normalize_operator(operator)

            self._parts["joins"].append({
                "type": join_type,
                "table": table,
                "alias": table_alias,
                "condition": (left_column, operator, right_column)
            })
            return self

        except Exception as e:
            if isinstance(e, (QueryError, ValidationError)):
                raise
            raise QueryError(f"Failed to add join: {str(e)}") from e

    def inner_join(self, table: str, table_alias: str = None, left_column: str = None,
                   operator: Union[str, Operator] = None, right_column: str = None) -> "SelectQuery":
        """Add an INNER JOIN."""
        return self.join(table, table_alias, left_column, operator, right_column, "INNER")

    def left_join(self, table: str, table_alias: str = None, left_column: str = None,
                  operator: Union[str, Operator] = None, right_column: str = None) -> "SelectQuery":
        """Add a LEFT JOIN."""
        return self.join(table, table_alias, left_column, operator, right_column, "LEFT")

    def right_join(self, table: str, table_alias: str = None, left_column: str = None,
                   operator: Union[str, Operator] = None, right_column: str = None) -> "SelectQuery":
        """Add a RIGHT JOIN."""
        return self.join(table, table_alias, left_column, operator, right_column, "RIGHT")

    def full_join(self, table: str, table_alias: str = None, left_column: str = None,
                  operator: Union[str, Operator] = None, right_column: str = None) -> "SelectQuery":
        """Add a FULL OUTER JOIN."""
        if not self._dialect.supports_full_outer_join:
            raise UnsupportedOperationError(
                f"FULL OUTER JOIN is not supported in {self._dialect.__class__.__name__}"
            )
        return self.join(table, table_alias, left_column, operator, right_column, "FULL OUTER")

    def where(self, column: str, operator: Union[str, Operator] = None, value: Any = None) -> "SelectQuery":
        """
        Add WHERE condition.

        Can be used in multiple ways:
        - where('age', '>', 18)
        - where('age > ?', 18)  # Future enhancement
        """
        if not column or not isinstance(column, str):
            raise ValidationError("Column must be a non-empty string")

        # Check for regex operator support immediately
        self._check_regex_support(operator)

        operator = self._normalize_operator(operator)
        self._parts["where"].append(("AND", (column, operator, value)))
        return self

    def or_where(self, column: str, operator: Union[str, Operator], value: Any) -> "SelectQuery":
        """Add OR WHERE condition."""
        if not column or not isinstance(column, str):
            raise ValidationError("Column must be a non-empty string")

        # Check for regex operator support immediately
        self._check_regex_support(operator)

        operator = self._normalize_operator(operator)
        self._parts["where"].append(("OR", (column, operator, value)))
        return self

    def where_in(self, column: str, values: List[Any]) -> "SelectQuery":
        """Add WHERE IN condition."""
        return self.where(column, "in", values)

    def where_not_in(self, column: str, values: List[Any]) -> "SelectQuery":
        """Add WHERE NOT IN condition."""
        return self.where(column, "not in", values)

    def where_null(self, column: str) -> "SelectQuery":
        """Add WHERE IS NULL condition."""
        return self.where(column, "is", None)

    def where_not_null(self, column: str) -> "SelectQuery":
        """Add WHERE IS NOT NULL condition."""
        return self.where(column, "is not", None)

    def where_between(self, column: str, start: Any, end: Any) -> "SelectQuery":
        """Add WHERE BETWEEN condition."""
        return self.where(column, "between", [start, end])

    def where_like(self, column: str, pattern: str) -> "SelectQuery":
        """Add WHERE LIKE condition."""
        return self.where(column, "like", pattern)

    def where_not_like(self, column: str, pattern: str) -> "SelectQuery":
        """Add WHERE NOT LIKE condition."""
        return self.where(column, "not like", pattern)

    def where_regex(self, column: str, pattern: str) -> "SelectQuery":
        """Add WHERE with regex matching."""
        # Check early for SQLite to raise error immediately
        if not self._dialect.supports_regex_operator:
            raise UnsupportedOperationError(
                f"Regex matching is not supported in {self._dialect.__class__.__name__}. "
                f"Consider using LIKE instead."
            )
        return self.where(column, "regex", pattern)

    # Additional shorthand methods for common operators
    def where_eq(self, column: str, value: Any) -> "SelectQuery":
        """Add WHERE = condition."""
        return self.where(column, "=", value)

    def where_ne(self, column: str, value: Any) -> "SelectQuery":
        """Add WHERE != condition."""
        return self.where(column, "!=", value)

    def where_lt(self, column: str, value: Any) -> "SelectQuery":
        """Add WHERE < condition."""
        return self.where(column, "<", value)

    def where_lte(self, column: str, value: Any) -> "SelectQuery":
        """Add WHERE <= condition."""
        return self.where(column, "<=", value)

    def where_gt(self, column: str, value: Any) -> "SelectQuery":
        """Add WHERE > condition."""
        return self.where(column, ">", value)

    def where_gte(self, column: str, value: Any) -> "SelectQuery":
        """Add WHERE >= condition."""
        return self.where(column, ">=", value)

    def group_by(self, *columns: str) -> "SelectQuery":
        """Add GROUP BY clause."""
        if not columns:
            raise ValidationError("GROUP BY requires at least one column")

        for col in columns:
            if not col or not isinstance(col, str):
                raise ValidationError(f"GROUP BY column must be a non-empty string, got: {col}")

        self._parts["group_by"].extend(columns)
        return self

    def having(self, column: str, operator: Union[str, Operator], value: Any) -> "SelectQuery":
        """Add HAVING condition."""
        if not column or not isinstance(column, str):
            raise ValidationError("Column must be a non-empty string")

        operator = self._normalize_operator(operator)
        self._parts["having"].append(("AND", (column, operator, value)))
        return self

    def order_by(self, column: str, direction: str = None) -> "SelectQuery":
        """
        Add ORDER BY clause.

        Can be used as:
        - order_by('name')  # defaults to ASC
        - order_by('name', 'DESC')
        - order_by('name DESC')  # parses direction from column
        """
        if not column or not isinstance(column, str):
            raise ValidationError("ORDER BY column must be a non-empty string")

        # Parse column and direction if provided as single string
        if ' ' in column and direction is None:
            parts = column.rsplit(' ', 1)
            if parts[1].upper() in ["ASC", "DESC"]:
                column = parts[0]
                direction = parts[1].upper()

        # Default direction
        if direction is None:
            direction = "ASC"
        elif direction.upper() not in ["ASC", "DESC"]:
            raise QueryError("ORDER BY direction must be ASC or DESC")

        self._parts["order_by"].append(f"{column} {direction.upper()}")
        return self

    def limit(self, count: int) -> "SelectQuery":
        """Add LIMIT clause."""
        if not isinstance(count, int) or count < 0:
            raise QueryError("LIMIT must be a non-negative integer")
        self._parts["limit"] = count
        return self

    def offset(self, count: int) -> "SelectQuery":
        """Add OFFSET clause."""
        if not isinstance(count, int) or count < 0:
            raise QueryError("OFFSET must be a non-negative integer")
        self._parts["offset"] = count
        return self

    def _build_sql(self) -> str:
        """Build SELECT SQL."""
        try:
            if not self._parts["from"]:
                raise QueryError("SELECT query must have a FROM clause")

            # SELECT clause
            select_cols = ", ".join(self._parts["select"])
            sql = f"SELECT {select_cols}"

            if self._parts["distinct"]:
                sql = f"SELECT DISTINCT {select_cols}"

            # FROM clause
            from_clause = self._parts['from']
            if self._parts['from_alias']:
                from_clause += f" AS {self._parts['from_alias']}"
            sql += f" FROM {from_clause}"

            # JOIN clauses
            for join in self._parts["joins"]:
                join_type = join["type"]
                table = join["table"]
                alias = join["alias"]
                left_col, op, right_col = join["condition"]

                # Build join condition
                condition = f"{left_col} {op.value} {right_col}"

                sql += f" {join_type} JOIN {table}"
                if alias:
                    sql += f" AS {alias}"
                sql += f" ON {condition}"

            # WHERE clause
            if self._parts["where"]:
                conditions = []
                for i, (logic, condition_data) in enumerate(self._parts["where"]):
                    column, operator, value = condition_data
                    condition = self._format_condition(column, operator, value)
                    if i == 0:
                        conditions.append(condition)
                    else:
                        conditions.append(f"{logic} {condition}")
                sql += f" WHERE {' '.join(conditions)}"

            # GROUP BY clause
            if self._parts["group_by"]:
                sql += f" GROUP BY {', '.join(self._parts['group_by'])}"

            # HAVING clause
            if self._parts["having"]:
                if not self._parts["group_by"]:
                    raise QueryError("HAVING clause requires GROUP BY")

                conditions = []
                for i, (logic, condition_data) in enumerate(self._parts["having"]):
                    column, operator, value = condition_data
                    condition = self._format_condition(column, operator, value)
                    if i == 0:
                        conditions.append(condition)
                    else:
                        conditions.append(f"{logic} {condition}")
                sql += f" HAVING {' '.join(conditions)}"

            # ORDER BY clause
            if self._parts["order_by"]:
                sql += f" ORDER BY {', '.join(self._parts['order_by'])}"

            # LIMIT/OFFSET clause
            if self._parts["limit"]:
                limit_clause = self._dialect.format_limit(
                    self._parts["limit"],
                    self._parts["offset"]
                )
                sql += f" {limit_clause}"

            return sql

        except Exception as e:
            if isinstance(e, (QueryError, ValidationError, UnsupportedOperationError)):
                raise
            raise QueryError(f"Failed to build SELECT query: {str(e)}") from e


class InsertQuery(Query):
    """INSERT query builder with CTE support."""

    def __init__(self, table: str, dialect: Union[str, Dialect]):
        super().__init__(dialect)
        self._type = "INSERT"
        self._table = table
        self._values = {}
        self._returning = []

    def values(self, data: Dict[str, Any]) -> "InsertQuery":
        """Set values to insert."""
        if not data:
            raise ValidationError("INSERT values cannot be empty")

        if not isinstance(data, dict):
            raise ValidationError("INSERT values must be a dictionary")

        # Validate column names
        for col in data.keys():
            if not col or not isinstance(col, str):
                raise ValidationError(f"Column name must be a non-empty string, got: {col}")

        self._values = data
        return self

    def returning(self, *columns: str) -> "InsertQuery":
        """Add RETURNING clause (PostgreSQL only)."""
        if not self._dialect.supports_returning:
            raise UnsupportedOperationError(
                f"RETURNING is not supported in {self._dialect.__class__.__name__}"
            )

        for col in columns:
            if not col or not isinstance(col, str):
                raise ValidationError(f"RETURNING column must be a non-empty string, got: {col}")

        self._returning.extend(columns)
        return self

    def _build_sql(self) -> str:
        """Build INSERT SQL."""
        try:
            if not self._values:
                raise QueryError("INSERT query must have values")

            columns = list(self._values.keys())
            placeholders = []

            for value in self._values.values():
                placeholders.append(self._add_param(value))

            columns_str = ", ".join(columns)
            values_str = ", ".join(placeholders)

            sql = f"INSERT INTO {self._table} ({columns_str}) VALUES ({values_str})"

            # RETURNING clause
            if self._returning:
                sql += f" RETURNING {', '.join(self._returning)}"

            return sql

        except Exception as e:
            if isinstance(e, (QueryError, ValidationError, UnsupportedOperationError)):
                raise
            raise QueryError(f"Failed to build INSERT query: {str(e)}") from e


class UpdateQuery(Query):
    """UPDATE query builder with CTE support."""

    def __init__(self, table: str, dialect: Union[str, Dialect]):
        super().__init__(dialect)
        self._type = "UPDATE"
        self._table = table
        self._set_values = {}
        self._where_conditions = []
        self._returning = []

    def set(self, data: Dict[str, Any]) -> "UpdateQuery":
        """Set values to update."""
        if not data:
            raise ValidationError("UPDATE SET values cannot be empty")

        if not isinstance(data, dict):
            raise ValidationError("UPDATE SET values must be a dictionary")

        # Validate column names
        for col in data.keys():
            if not col or not isinstance(col, str):
                raise ValidationError(f"Column name must be a non-empty string, got: {col}")

        self._set_values = data
        return self

    def where(self, column: str, operator: Union[str, Operator] = None, value: Any = None) -> "UpdateQuery":
        """Add WHERE condition with string operator support."""
        if not column or not isinstance(column, str):
            raise ValidationError("Column must be a non-empty string")

        # Check for regex operator support immediately
        self._check_regex_support(operator)

        operator = self._normalize_operator(operator)
        self._where_conditions.append(("AND", (column, operator, value)))
        return self

    def or_where(self, column: str, operator: Union[str, Operator], value: Any) -> "UpdateQuery":
        """Add OR WHERE condition."""
        if not column or not isinstance(column, str):
            raise ValidationError("Column must be a non-empty string")

        # Check for regex operator support immediately
        self._check_regex_support(operator)

        operator = self._normalize_operator(operator)
        self._where_conditions.append(("OR", (column, operator, value)))
        return self

    def where_in(self, column: str, values: List[Any]) -> "UpdateQuery":
        """Add WHERE IN condition."""
        return self.where(column, "in", values)

    def where_eq(self, column: str, value: Any) -> "UpdateQuery":
        """Add WHERE = condition."""
        return self.where(column, "=", value)

    def where_regex(self, column: str, pattern: str) -> "UpdateQuery":
        """Add WHERE with regex matching."""
        # Check early for SQLite to raise error immediately
        if not self._dialect.supports_regex_operator:
            raise UnsupportedOperationError(
                f"Regex matching is not supported in {self._dialect.__class__.__name__}. "
                f"Consider using LIKE instead."
            )
        return self.where(column, "regex", pattern)

    def returning(self, *columns: str) -> "UpdateQuery":
        """Add RETURNING clause (PostgreSQL only)."""
        if not self._dialect.supports_returning:
            raise UnsupportedOperationError(
                f"RETURNING is not supported in {self._dialect.__class__.__name__}"
            )

        for col in columns:
            if not col or not isinstance(col, str):
                raise ValidationError(f"RETURNING column must be a non-empty string, got: {col}")

        self._returning.extend(columns)
        return self

    def _build_sql(self) -> str:
        """Build UPDATE SQL."""
        try:
            if not self._set_values:
                raise QueryError("UPDATE query must have SET values")

            # SET clause first
            set_clauses = []
            for column, value in self._set_values.items():
                placeholder = self._add_param(value)
                set_clauses.append(f"{column} = {placeholder}")

            sql = f"UPDATE {self._table} SET {', '.join(set_clauses)}"

            # WHERE clause - build conditions with correct parameter order
            if self._where_conditions:
                conditions = []
                for i, (logic, condition_data) in enumerate(self._where_conditions):
                    column, operator, value = condition_data
                    condition = self._format_condition(column, operator, value)
                    if i == 0:
                        conditions.append(condition)
                    else:
                        conditions.append(f"{logic} {condition}")
                sql += f" WHERE {' '.join(conditions)}"
            else:
                # Warn about UPDATE without WHERE clause
                import warnings
                warnings.warn(
                    "UPDATE query without WHERE clause will update all rows. "
                    "Use where() to add conditions.",
                    UserWarning
                )

            # RETURNING clause
            if self._returning:
                sql += f" RETURNING {', '.join(self._returning)}"

            return sql

        except Exception as e:
            if isinstance(e, (QueryError, ValidationError, UnsupportedOperationError)):
                raise
            raise QueryError(f"Failed to build UPDATE query: {str(e)}") from e


class DeleteQuery(Query):
    """DELETE query builder with CTE support."""

    def __init__(self, table: str, dialect: Union[str, Dialect]):
        super().__init__(dialect)
        self._type = "DELETE"
        self._table = table
        self._where_conditions = []
        self._returning = []

    def where(self, column: str, operator: Union[str, Operator] = None, value: Any = None) -> "DeleteQuery":
        """Add WHERE condition with string operator support."""
        if not column or not isinstance(column, str):
            raise ValidationError("Column must be a non-empty string")

        # Check for regex operator support immediately
        self._check_regex_support(operator)

        operator = self._normalize_operator(operator)
        self._where_conditions.append(("AND", (column, operator, value)))
        return self

    def or_where(self, column: str, operator: Union[str, Operator], value: Any) -> "DeleteQuery":
        """Add OR WHERE condition."""
        if not column or not isinstance(column, str):
            raise ValidationError("Column must be a non-empty string")

        # Check for regex operator support immediately
        self._check_regex_support(operator)

        operator = self._normalize_operator(operator)
        self._where_conditions.append(("OR", (column, operator, value)))
        return self

    def where_in(self, column: str, values: List[Any]) -> "DeleteQuery":
        """Add WHERE IN condition."""
        return self.where(column, "in", values)

    def where_not_in(self, column: str, values: List[Any]) -> "DeleteQuery":
        """Add WHERE NOT IN condition."""
        return self.where(column, "not in", values)

    def where_eq(self, column: str, value: Any) -> "DeleteQuery":
        """Add WHERE = condition."""
        return self.where(column, "=", value)

    def where_regex(self, column: str, pattern: str) -> "DeleteQuery":
        """Add WHERE with regex matching."""
        # Check early for SQLite to raise error immediately
        if not self._dialect.supports_regex_operator:
            raise UnsupportedOperationError(
                f"Regex matching is not supported in {self._dialect.__class__.__name__}. "
                f"Consider using LIKE instead."
            )
        return self.where(column, "regex", pattern)

    def returning(self, *columns: str) -> "DeleteQuery":
        """Add RETURNING clause (PostgreSQL specific)."""
        if not self._dialect.supports_returning:
            raise UnsupportedOperationError(
                f"RETURNING is not supported in {self._dialect.__class__.__name__}"
            )

        for col in columns:
            if not col or not isinstance(col, str):
                raise ValidationError(f"RETURNING column must be a non-empty string, got: {col}")

        self._returning.extend(columns)
        return self

    def _build_sql(self) -> str:
        """Build DELETE SQL."""
        try:
            sql = f"DELETE FROM {self._table}"

            # WHERE clause
            if self._where_conditions:
                conditions = []
                for i, (logic, condition_data) in enumerate(self._where_conditions):
                    column, operator, value = condition_data
                    condition = self._format_condition(column, operator, value)
                    if i == 0:
                        conditions.append(condition)
                    else:
                        conditions.append(f"{logic} {condition}")
                sql += f" WHERE {' '.join(conditions)}"
            else:
                # Warn about DELETE without WHERE clause
                import warnings
                warnings.warn(
                    "DELETE query without WHERE clause will delete all rows. "
                    "Use where() to add conditions.",
                    UserWarning
                )

            # RETURNING clause
            if self._returning:
                sql += f" RETURNING {', '.join(self._returning)}"

            return sql

        except Exception as e:
            if isinstance(e, (QueryError, ValidationError, UnsupportedOperationError)):
                raise
            raise QueryError(f"Failed to build DELETE query: {str(e)}") from e