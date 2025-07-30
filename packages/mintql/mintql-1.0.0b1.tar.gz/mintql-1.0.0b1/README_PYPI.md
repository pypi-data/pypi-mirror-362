# MintQL

**A minimalist SQL query builder for Python**

[![PyPI - Version](https://img.shields.io/pypi/v/mintql?color=green)](https://pypi.org/project/mintql/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/mintql)](https://pypi.org/project/mintql/)
[![License](https://img.shields.io/badge/license-MIT-blue)](https://github.com/yourusername/mintql/blob/main/LICENSE)

---

## What is MintQL?

MintQL is a lightweight, type-safe SQL query builder designed to produce clean and parameterized SQL queries, helping to avoid common pitfalls such as string concatenation and injection vulnerabilities. **MintQL is NOT an ORM.**

### Why MintQL?
- **Tiny learning curve** - if you know SQL, you know MintQL
- **Zero dependencies** - build in pure Python
- **You keep control over your SQL** - see exactly what queries are generated

### Key Features
- **SQL injection protection** through parameterized queries
- **Type-safe** query building with IDE autocompletion  
- **Multi-dialect support** (PostgreSQL, MySQL, SQLite)
- **Fluent API** for readable query construction
- **CTE support** including recursive CTEs
- **Zero dependencies** - lightweight and fast

## Installation

```bash
pip install mintql
```

**Requirements:**
- Python 3.8 or higher
- No external dependencies!

## Quick Start

```python
from mintql import pg

# Build your query
query = pg.select('name', 'email').from_('users').where('active', '=', True)

# Get SQL and parameters
sql, params = query.build()
# sql: "SELECT name, email FROM users WHERE active = $1"
# params: [True]

# Use with any PostgreSQL driver (psycopg2, asyncpg, etc.)
cursor.execute(sql, params)
```

## MintQL vs ORMs

### What MintQL IS:
- A **query builder** that generates clean, safe SQL
- A thin layer over SQL that adds safety and convenience
- Perfect for developers who want to write SQL without string manipulation

### What MintQL IS NOT:
- ❌ An ORM - no models, no migrations, no magic
- ❌ A database abstraction layer - you still write SQL logic
- ❌ A schema manager


## Basic Usage

### SELECT Queries

```python
from mintql import pg

# Simple SELECT
query = pg.select('*').from_('users')

# With conditions
query = (pg.select('id', 'name', 'email')
         .from_('users')
         .where('active', '=', True)
         .where('age', '>=', 18)
         .order_by('name'))

# Build and execute
sql, params = query.build()
# sql: "SELECT id, name, email FROM users WHERE active = $1 AND age >= $2 ORDER BY name ASC"
# params: [True, 18]
```

### INSERT Operations

```python
# Single insert
query = pg.insert('users').values({
    'name': 'Jane Doe',
    'email': 'jane@example.com',
    'active': True
})

# With RETURNING (PostgreSQL)
query = (pg.insert('users')
         .values({'name': 'John', 'email': 'john@example.com'})
         .returning('id', 'created_at'))
```

### UPDATE Operations

```python
query = (pg.update('users')
         .set({'last_login': 'NOW()', 'login_count': 'login_count + 1'})
         .where('id', '=', user_id))
```

### DELETE Operations

```python
query = pg.delete('users').where('active', '=', False).where('created_at', '<', '2023-01-01')
```

## Integration Examples

### psycopg2 (PostgreSQL)

```python
import psycopg2
from mintql import pg

# Connect to your database
conn = psycopg2.connect("dbname=myapp user=postgres")
cur = conn.cursor()

# Build your query
query = (pg.select('u.name', 'COUNT(o.id) as order_count')
         .from_('users u')
         .left_join('orders o ON u.id = o.user_id')
         .where('u.created_at', '>=', '2024-01-01')
         .group_by('u.id', 'u.name')
         .having('COUNT(o.id)', '>', 5))

# Execute
sql, params = query.build()
cur.execute(sql, params)
results = cur.fetchall()
```

### MySQL

```python
import mysql.connector
from mintql import mysql

conn = mysql.connector.connect(host='localhost', database='myapp')
cursor = conn.cursor()

query = mysql.select('*').from_('products').where('price', '<', 100)
sql, params = query.build()

# MySQL uses ? placeholders
cursor.execute(sql, params)
```

### SQLite

```python
import sqlite3
from mintql import sqlite

conn = sqlite3.connect('myapp.db')
cursor = conn.cursor()

query = sqlite.select('*').from_('users').limit(10)
sql, params = query.build()

cursor.execute(sql, params)
```

## Advanced Features

### CTEs (Common Table Expressions)

```python
# Simple CTE
subquery = (pg.select('department', 'AVG(salary) as avg_salary')
            .from_('employees')
            .group_by('department'))

query = (pg.select('*')
         .with_('dept_averages', subquery)
         .from_('dept_averages')
         .where('avg_salary', '>', 50000))

# Recursive CTE
anchor = pg.select('id', 'name', 'manager_id', '0 as level').from_('employees').where('manager_id', 'is', None)
recursive = pg.select('e.id', 'e.name', 'e.manager_id', 'h.level + 1').from_('employees e').inner_join('hierarchy h ON e.manager_id = h.id')

query = (pg.select('*')
         .with_recursive('hierarchy', anchor, recursive)
         .from_('hierarchy')
         .order_by('level'))
```

### Complex JOINs

```python
query = (pg.select('u.name', 'p.title', 'c.content')
         .from_('users u')
         .inner_join('posts p ON u.id = p.user_id')
         .left_join('comments c ON p.id = c.post_id')
         .where('u.active', '=', True)
         .where('p.published', '=', True)
         .order_by('p.created_at', 'DESC'))
```

### Using Operators & Functions

```python
from mintql import pg, O, F

# Operators
query = (pg.select('*')
         .from_('users')
         .where('age', O.BETWEEN, [18, 65])
         .where('email', O.LIKE, '%@example.com')
         .where('role', O.IN, ['admin', 'moderator']))

# Functions
query = (pg.select(
            F.COUNT('*').as_('total'),
            F.AVG('age').as_('avg_age'),
            F.MAX('created_at').as_('latest')
         )
         .from_('users')
         .where(F.YEAR('created_at'), '=', 2024))
```

## Safety Features

### SQL Injection Protection

MintQL automatically parameterizes all values:

```python
# User input is safely parameterized
user_input = "'; DROP TABLE users; --"
query = pg.select('*').from_('users').where('name', '=', user_input)

sql, params = query.build()
# sql: "SELECT * FROM users WHERE name = $1"
# params: ["'; DROP TABLE users; --"]  # Safely escaped!
```

### Type Validation

```python
# ✅ Valid
query = pg.select('*').from_('users').where('id', 'IN', [1, 2, 3])

# ❌ Raises ValidationError
query = pg.select('*').from_('users').where('id', 'IN', 'not-a-list')
```

## Error Handling

```python
from mintql import pg
from mintql.exceptions import QueryError, ValidationError, UnsupportedOperationError

try:
    # Invalid operator
    query = pg.select('*').from_('users').where('age', 'INVALID_OP', 25)
except QueryError as e:
    print(f"Query construction error: {e}")

try:
    # Validation error
    query = pg.select('*').from_('')  # Empty table name
except ValidationError as e:
    print(f"Validation error: {e}")

try:
    # Unsupported operation for dialect
    query = sqlite.select('*').from_('users').returning('id')  # SQLite doesn't support RETURNING
except UnsupportedOperationError as e:
    print(f"Not supported: {e}")
```

## Multi-Dialect Support

**PostgreSQL, MySQL, and SQLite**

MintQL handles dialect differences automatically:

```python
from mintql import MintQL

# Create dialect-specific instances
pg_query = MintQL.postgresql()
mysql_query = MintQL.mysql()
sqlite_query = MintQL.sqlite()

# Or use shortcuts
from mintql import pg, mysql, sqlite

# Same API, different SQL outputs
pg.select('*').from_('users').where('id', '=', 1)
# PostgreSQL: SELECT * FROM users WHERE id = $1

mysql.select('*').from_('users').where('id', '=', 1)  
# MySQL: SELECT * FROM users WHERE id = ?

sqlite.select('*').from_('users').where('id', '=', 1)
# SQLite: SELECT * FROM users WHERE id = ?
```

## Full Documentation

Coming Soon

## When to use MintQL?

**Perfect for:**
- Projects where you want to write SQL but safely
- Applications with complex queries
- Teams that want readable, maintainable database code
- Scripts and tools that need simple database queries

**Consider alternatives for:**
- Projects that need full ORM features (relationships, lazy loading)
- Applications requiring automatic schema migration

## License

MintQL is MIT licensed. See [LICENSE](LICENSE) for details.

## Links

- [GitHub](https://github.com/thomasfazzari1/mintql)
- [PyPI](https://pypi.org/project/mintql/)
- Full Documentation (coming soon)