"""
Main Mint factory class providing the fluent API.
"""

from typing import Union, Any, Dict, List
from .dialects import Dialect, Dialects, get_dialect, PostgreSQLDialect, MySQLDialect, SQLiteDialect
from .exceptions import MintqlError


class MintQL:
    """
    Main factory class for creating SQL queries.

    Provides a fluent interface for building SELECT, INSERT, UPDATE, and DELETE queries
    with automatic SQL injection protection.

    Example:
        >>> from mintql import MintQL
        >>> mint_pg = MintQL.postgresql()
        >>> query = mint_pg.select('id', 'name').from_('users')
        >>> sql, params = query.build()
    """

    def __init__(self, dialect: Union[str, Dialects, Dialect]):
        """
        Initialize Mint with a specific dialect.

        Args:
            dialect: Can be:
                - A Dialects enum value: Dialects.POSTGRESQL
                - A string name: 'postgresql', 'mysql', 'sqlite'
                - A Dialect instance for custom dialects

        Example:
            >>> mint_pg = MintQL('postgresql')
            >>> mint_pg = MintQL(Dialects.POSTGRESQL)
            >>> mint_pg = MintQL.postgresql()  # Recommended
        """
        if dialect is None:
            raise MintqlError("Dialect must be provided")

        if isinstance(dialect, Dialect):
            self._dialect = dialect
        elif isinstance(dialect, (str, Dialects)):
            self._dialect = get_dialect(dialect)
        else:
            raise TypeError(
                f"Dialect must be a Dialects enum, string, or Dialect instance, got {type(dialect)}. "
                f"Use: Mint('postgresql'), Mint(Dialects.POSTGRESQL), or Mint.postgresql()"
            )

    # Factory methods for safer instantiation
    @classmethod
    def postgresql(cls) -> "MintQL":
        """Create a Mint instance for PostgreSQL."""
        return cls(PostgreSQLDialect())

    @classmethod
    def postgres(cls) -> "MintQL":
        """Create a Mint instance for PostgreSQL (alias)."""
        return cls.postgresql()

    @classmethod
    def pg(cls) -> "MintQL":
        """Create a Mint instance for PostgreSQL (alias)."""
        return cls.postgresql()

    @classmethod
    def mysql(cls) -> "MintQL":
        """Create a Mint instance for MySQL."""
        return cls(MySQLDialect())

    @classmethod
    def sqlite(cls) -> "MintQL":
        """Create a Mint instance for SQLite."""
        return cls(SQLiteDialect())

    def select(self, *columns: str) -> "SelectQuery":
        """
        Create a SELECT query.

        Args:
            *columns: Column names to select. If none provided, selects all (*).

        Returns:
            SelectQuery: A new SELECT query builder.

        Example:
            >>> mint = MintQL.postgresql()
            >>> query = mint.select("id", "name").from_("users")
            >>> sql, params = query.build()
            >>> print(sql)  # SELECT id, name FROM users
        """

        from .query import SelectQuery

        query = SelectQuery(self._dialect)
        if columns:
            query.select(*columns)
        else:
            query.select()  # Becomes SELECT *
        return query

    def insert(self, table: str) -> "InsertQuery":
        """
        Create an INSERT query.

        Args:
            table: Table name to insert into.

        Returns:
            InsertQuery: A new INSERT query builder.

        Example:
            >>> mint_pg = MintQL.postgresql()
            >>> query = mint_pg.insert("users").values({"name": "John", "age": 30})
            >>> sql, params = query.build()
            >>> print(sql)  # INSERT INTO users (name, age) VALUES ($1, $2)
        """
        from .query import InsertQuery

        return InsertQuery(table, self._dialect)

    def update(self, table: str) -> "UpdateQuery":
        """
        Create an UPDATE query.

        Args:
            table: Table name to update.

        Returns:
            UpdateQuery: A new UPDATE query builder.

        Example:
            >>> mint = MintQL.postgresql()
            >>> query = mint.update("users").set({"name": "Jane"}).where("id", "=", 1)
            >>> sql, params = query.build()
            >>> print(sql)  # UPDATE users SET name = $1 WHERE id = $2
        """
        from .query import UpdateQuery

        return UpdateQuery(table, self._dialect)

    def delete(self, table: str) -> "DeleteQuery":
        """
        Create a DELETE query.

        Args:
            table: Table name to delete from.

        Returns:
            DeleteQuery: A new DELETE query builder.

        Example:
            >>> mint_pg = MintQL.postgresql()
            >>> query = mint_pg.delete("users").where("active", "=", False)
            >>> sql, params = query.build()
            >>> print(sql)  # DELETE FROM users WHERE active = $1
        """
        from .query import DeleteQuery

        return DeleteQuery(table, self._dialect)


# Premade instances
pg = MintQL.postgresql()
postgres = MintQL.postgresql()
postgresql = MintQL.postgresql()
mysql = MintQL.mysql()
sqlite = MintQL.sqlite()