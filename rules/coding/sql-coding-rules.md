---
name: SQL Coding Rules
version: 1.0.0
author: Mathias Paulenko Echeverz
description: Coding standards for SQL queries. Covers naming conventions, indexing guidelines, query optimization, CTE usage, and anti-patterns to avoid.
tags: [sql, database, coding-rules, query-optimization, indexing, performance]
role: coding-standard
type: rules
language: en
---

# SQL Coding Rules

## 1. Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Tables | `snake_case`, plural | `users`, `order_items` |
| Columns | `snake_case` | `created_at`, `email_verified` |
| Primary keys | `id` or `{table}_id` | `id`, `user_id` |
| Foreign keys | `{referenced_table}_id` | `user_id`, `product_id` |
| Indexes | `idx_{table}_{column}` | `idx_users_email` |
| Constraints | `chk_{table}_{rule}` / `fk_{table}_{ref}` | `chk_users_age_positive` |
| Views | `vw_{description}` | `vw_active_users` |
| Functions | `fn_{description}` | `fn_calculate_age` |
| Stored procedures | `sp_{description}` | `sp_process_order` |

## 2. Query Structure

- Use **uppercase** for SQL keywords (`SELECT`, `FROM`, `WHERE`).
- Place each clause on a new line.
- Indent subqueries and JOIN conditions.
- Alias tables in JOINs for readability.

```sql
-- Good
SELECT
  u.id,
  u.email,
  COUNT(o.id) AS order_count,
  SUM(o.total) AS lifetime_value
FROM users AS u
LEFT JOIN orders AS o ON o.user_id = u.id
WHERE u.created_at >= '2024-01-01'
  AND u.is_active = TRUE
GROUP BY u.id, u.email
HAVING COUNT(o.id) > 0
ORDER BY lifetime_value DESC
LIMIT 100;

-- Bad
select id,email,count(o.id) from users u left join orders o on o.user_id=u.id where u.created_at>='2024-01-01' group by u.id order by sum(o.total) desc limit 100;
```

## 3. Indexing

### When to Index

- Columns used in `WHERE`, `JOIN`, `ORDER BY`, `GROUP BY`.
- Foreign keys (automatically indexed in some engines; verify).
- Columns with high cardinality (many distinct values).

### When NOT to Index

- Columns with low cardinality (boolean flags, status enums).
- Frequently updated columns (indexes add write overhead).
- Small tables (full scan may be faster).

### Composite Indexes

- Order columns by selectivity (most selective first).
- Match index order to query predicates.

```sql
-- Good — matches WHERE user_id = ? AND created_at BETWEEN ? AND ?
CREATE INDEX idx_orders_user_created
  ON orders (user_id, created_at);

-- Bad — created_at first is less selective
CREATE INDEX idx_orders_created_user
  ON orders (created_at, user_id);
```

## 4. Query Optimization

### SELECT Specific Columns

```sql
-- Good
SELECT id, name, email FROM users;

-- Bad
SELECT * FROM users;
```

### Use EXISTS Instead of COUNT for Existence Checks

```sql
-- Good
SELECT 1 FROM users WHERE email = 'test@example.com' LIMIT 1;

-- Bad
SELECT COUNT(*) FROM users WHERE email = 'test@example.com';
```

### Use JOINs Over Subqueries Where Possible

```sql
-- Good
SELECT u.name, o.total
FROM users u
JOIN orders o ON o.user_id = u.id;

-- Bad
SELECT name,
  (SELECT total FROM orders WHERE user_id = users.id)
FROM users;
```

### Avoid Functions on Indexed Columns

```sql
-- Bad — prevents index usage
SELECT * FROM users WHERE YEAR(created_at) = 2024;

-- Good — range scan on index
SELECT * FROM users
WHERE created_at >= '2024-01-01'
  AND created_at < '2025-01-01';
```

## 5. Common Table Expressions (CTEs)

- Use CTEs for readability and recursion.
- Prefer CTEs over nested subqueries.
- Materialize CTEs only when necessary.

```sql
WITH monthly_stats AS (
  SELECT
    DATE_TRUNC('month', created_at) AS month,
    COUNT(*) AS order_count,
    SUM(total) AS revenue
  FROM orders
  WHERE created_at >= CURRENT_DATE - INTERVAL '12 months'
  GROUP BY DATE_TRUNC('month', created_at)
),
growth AS (
  SELECT
    month,
    order_count,
    revenue,
    LAG(revenue) OVER (ORDER BY month) AS prev_revenue
  FROM monthly_stats
)
SELECT
  month,
  order_count,
  revenue,
  ROUND(
    (revenue - prev_revenue) / prev_revenue * 100,
    2
  ) AS growth_pct
FROM growth
ORDER BY month;
```

## 6. Anti-Patterns to Avoid

| Anti-Pattern | Why It's Bad | Solution |
|-------------|--------------|----------|
| `SELECT *` | Breaks when schema changes; fetches unnecessary data | List specific columns |
| `N+1 queries` | Multiple round-trips; poor performance | Use JOINs or batch fetching |
| Implicit JOINs | Harder to read; error-prone | Use explicit `JOIN` syntax |
| Missing `LIMIT` on large tables | Unbounded result sets | Always paginate or limit |
| `NOT IN` with NULLs | Returns empty results unexpectedly | Use `NOT EXISTS` |
| String concatenation in queries | SQL injection risk | Use parameterized queries |
| `ORDER BY RAND()` | Full table sort; terrible performance | Use application-level randomization |
| `OR` on different indexed columns | Cannot use both indexes efficiently | Use `UNION` or redesign |

## 7. Transactions

- Keep transactions as short as possible.
- Use appropriate isolation levels.
- Handle deadlocks with retry logic.

```sql
BEGIN;

UPDATE inventory
SET quantity = quantity - 1
WHERE product_id = 123 AND quantity > 0;

IF NOT FOUND THEN
  RAISE EXCEPTION 'Insufficient inventory for product 123';
END IF;

INSERT INTO orders (user_id, product_id, quantity)
VALUES (1, 123, 1);

COMMIT;
```

## 8. Migrations

- Use migration tools (Flyway, Alembic, Liquibase).
- Never modify existing migration files after deployment.
- Make migrations reversible (down scripts).
- Test migrations on a copy of production data.

```sql
-- V20240604__add_user_verified.sql
ALTER TABLE users
ADD COLUMN email_verified BOOLEAN NOT NULL DEFAULT FALSE;

-- V20240604__add_user_verified.rollback.sql
ALTER TABLE users DROP COLUMN email_verified;
```

## 9. Security

- Use **parameterized queries** exclusively.
- Never concatenate user input into SQL strings.
- Use least-privilege database users.
- Encrypt sensitive columns (PII, credentials).

```python
# Good
cursor.execute("SELECT * FROM users WHERE email = %s", (user_email,))

# Bad — SQL injection
cursor.execute(f"SELECT * FROM users WHERE email = '{user_email}'")
```

## 10. Documentation

- Document complex queries with comments.
- Explain the business purpose, not the mechanics.
- Include expected execution plan notes for optimization work.

```sql
-- Find users who made their first purchase in the last 30 days
-- Used by: Marketing dashboard, Daily report
-- Performance: Index on orders(user_id, created_at) recommended
SELECT DISTINCT u.id, u.email
FROM users u
JOIN orders o ON o.user_id = u.id
WHERE o.created_at >= CURRENT_DATE - INTERVAL '30 days'
  AND NOT EXISTS (
    SELECT 1 FROM orders o2
    WHERE o2.user_id = u.id
      AND o2.created_at < CURRENT_DATE - INTERVAL '30 days'
  );
```
