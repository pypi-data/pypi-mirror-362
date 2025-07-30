"""
MintQL - A lightweight, type-safe SQL query builder designed to produce clean and parameterized SQL queries.

Basic usage:
    >>> from mintql import pg
    >>> query = pg.select('id', 'name').from_('users').where('age', '>', 18)
    >>> sql, params = query.build()

Or with factory methods:
    >>> from mintql import MintQL
    >>> mint_pg = MintQL.postgresql()
    >>> query = mint_pg.select('*').from_('users')

Or with string operators:
    >>> query = mint_pg.select('*').from_('users u').inner_join('orders o ON u.id = o.user_id')
"""

__version__ = "1.0.0b1"
__author__ = "Thomas Fazzari"

from .mintql import MintQL, pg, postgres, postgresql, mysql, sqlite
from .dialects import Dialects
from .operators import Operators, O
from .functions import Functions, F
from .exceptions import (
    MintqlError,
    QueryError,
    DialectError,
    ValidationError,
    UnsupportedOperationError
)

# Pre-configured dialect instances
from .mintql import pg, postgres, postgresql, mysql, sqlite

__all__ = [
    "MintQL",

    "pg",
    "postgres",
    "postgresql",
    "mysql",
    "sqlite",

    "Dialects",

    # Operators
    "Operators",
    "O",

    # Functions
    "Functions",
    "F",

    # Exceptions
    "MintqlError",
    "QueryError",
    "DialectError",
    "ValidationError",
    "UnsupportedOperationError",
]