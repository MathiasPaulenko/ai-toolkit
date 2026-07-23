---
name: sql-server
version: 1.0.0
author: Mathias Paulenko Echeverz
description: Microsoft SQL Server development guide. Covers T-SQL syntax, stored procedures, indexing strategies, temporal tables, JSON support, Always Encrypted, and Azure SQL specifics.
tags: [sql-server, t-sql, mssql, database, azure-sql, stored-procedures]
role: database-developer
model: any
trigger: When the user mentions SQL Server, T-SQL, MSSQL, Azure SQL, stored procedures, temporal tables, or SQL Server-specific features.
---

# SQL Server

## 1. T-SQL Basics

### SELECT with OFFSET/FETCH

```sql
SELECT id, name, email
FROM users
ORDER BY created_at DESC
OFFSET 40 ROWS FETCH NEXT 20 ROWS ONLY;  -- Page 3, 20 per page
```

### MERGE (Upsert)

```sql
MERGE users AS target
USING staging_users AS source
ON target.email = source.email
WHEN MATCHED THEN
    UPDATE SET target.name = source.name, target.updated_at = GETDATE()
WHEN NOT MATCHED THEN
    INSERT (email, name, created_at)
    VALUES (source.email, source.name, GETDATE());
```

### TRY/CATCH

```sql
BEGIN TRY
    BEGIN TRANSACTION;
    INSERT INTO orders (user_id, total) VALUES (1, 100.00);
    COMMIT TRANSACTION;
END TRY
BEGIN CATCH
    ROLLBACK TRANSACTION;
    THROW;  -- Re-raise the error
END CATCH;
```

## 2. Stored Procedures

```sql
CREATE PROCEDURE usp_GetUserOrders
    @UserId INT,
    @Status VARCHAR(20) = NULL,
    @PageNumber INT = 1,
    @PageSize INT = 20
AS
BEGIN
    SET NOCOUNT ON;

    SELECT o.id, o.total, o.status, o.created_at
    FROM orders o
    WHERE o.user_id = @UserId
      AND (@Status IS NULL OR o.status = @Status)
    ORDER BY o.created_at DESC
    OFFSET (@PageNumber - 1) * @PageSize ROWS
    FETCH NEXT @PageSize ROWS ONLY;

    SELECT COUNT(*) AS total_count
    FROM orders
    WHERE user_id = @UserId
      AND (@Status IS NULL OR status = @Status);
END;
GO
```

## 3. Indexing

| Type | Use Case |
|------|----------|
| Clustered | Primary key; determines physical sort order |
| Non-clustered | Additional lookup paths |
| Filtered | Index subset of rows (e.g., `WHERE is_active = 1`) |
| Columnstore | Analytical queries on large datasets |
| XML/JSON | Index XML columns or JSON paths |

```sql
-- Filtered index for active users
CREATE NONCLUSTERED INDEX IX_users_active_email
ON users(email)
WHERE is_active = 1;

-- Covering index
CREATE NONCLUSTERED INDEX IX_orders_user_status_covering
ON orders(user_id, status)
INCLUDE (total, created_at);  -- No key lookup needed
```

## 4. JSON Support

```sql
-- Parse JSON
DECLARE @json NVARCHAR(MAX) = '[{"id":1,"name":"Alice"},{"id":2,"name":"Bob"}]';

SELECT *
FROM OPENJSON(@json)
WITH (
    id INT '$.id',
    name VARCHAR(100) '$.name'
);

-- Store JSON
INSERT INTO events (data)
VALUES (JSON_OBJECT('action': 'login', 'user_id': 42));

-- Query JSON
SELECT id, JSON_VALUE(data, '$.action') AS action
FROM events
WHERE JSON_VALUE(data, '$.action') = 'login';
```

## 5. Temporal Tables (System-Versioning)

```sql
CREATE TABLE users (
    id INT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(255),
    valid_from DATETIME2 GENERATED ALWAYS AS ROW START HIDDEN,
    valid_to DATETIME2 GENERATED ALWAYS AS ROW END HIDDEN,
    PERIOD FOR SYSTEM_TIME (valid_from, valid_to)
) WITH (SYSTEM_VERSIONING = ON (HISTORY_TABLE = dbo.users_history));

-- Query as of a point in time
SELECT * FROM users
FOR SYSTEM_TIME AS OF '2024-01-15';
```

## 6. Always Encrypted

```sql
-- Column encrypted with deterministic encryption (allows equality)
CREATE TABLE patients (
    id INT PRIMARY KEY,
    ssn VARCHAR(11) COLLATE Latin1_General_BIN2
        ENCRYPTED WITH (
            COLUMN_ENCRYPTION_KEY = CEK1,
            ENCRYPTION_TYPE = DETERMINISTIC,
            ALGORITHM = 'AEAD_AES_256_CBC_HMAC_SHA_256'
        ),
    birth_date DATE
        ENCRYPTED WITH (
            COLUMN_ENCRYPTION_KEY = CEK1,
            ENCRYPTION_TYPE = RANDOMIZED,
            ALGORITHM = 'AEAD_AES_256_CBC_HMAC_SHA_256'
        )
);
```

## 7. Python Integration (pyodbc)

```python
import pyodbc

conn_str = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=myserver.database.windows.net;"
    "DATABASE=mydb;"
    "UID=myuser;PWD=mypassword"
)

with pyodbc.connect(conn_str) as conn:
    cursor = conn.cursor()
    cursor.execute(
        "EXEC usp_GetUserOrders ?, ?, ?, ?",
        (1, "completed", 1, 20),
    )
    rows = cursor.fetchall()
```

## 8. Azure SQL Specifics

- Use **Azure Active Directory authentication** for service principals.
- Enable **hyperscale** for databases > 100 GB.
- Use **serverless** tier for intermittent workloads.
- Configure **firewall rules** at server level, not database level.
- Use **connection retry logic** with exponential backoff (transient fault handling).

```python
# Connection retry with tenacity
from tenacity import retry, wait_exponential, stop_after_attempt

@retry(wait=wait_exponential(multiplier=1, min=4, max=10),
       stop=stop_after_attempt(3))
def execute_query(sql):
    with pyodbc.connect(conn_str) as conn:
        return conn.execute(sql).fetchall()
```
