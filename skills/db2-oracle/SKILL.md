---
name: db2-oracle
version: 1.0.0
author: Mathias Paulenko Echeverz
description: Enterprise database development for IBM DB2 and Oracle. Covers PL/SQL, SQL/PL, partitioning, performance tuning, XML/JSON handling, and migration patterns.
tags: [db2, oracle, plsql, database, enterprise, partitioning]
role: database-developer
model: any
trigger: When the user mentions DB2, Oracle, PL/SQL, SQL/PL, Oracle partitioning, DB2 pureScale, or enterprise database specifics.
---

# DB2 and Oracle

## 1. Oracle PL/SQL

### Basic Procedure

```sql
CREATE OR REPLACE PROCEDURE sp_create_order (
    p_user_id   IN  NUMBER,
    p_total     IN  NUMBER,
    p_order_id  OUT NUMBER
) AS
BEGIN
    INSERT INTO orders (user_id, total, status, created_at)
    VALUES (p_user_id, p_total, 'pending', SYSTIMESTAMP)
    RETURNING id INTO p_order_id;

    COMMIT;
EXCEPTION
    WHEN DUP_VAL_ON_INDEX THEN
        RAISE_APPLICATION_ERROR(-20001, 'Duplicate order detected');
    WHEN OTHERS THEN
        ROLLBACK;
        RAISE;
END;
/
```

### Cursor and Bulk Collect

```sql
DECLARE
    TYPE t_user_tab IS TABLE OF users%ROWTYPE;
    v_users t_user_tab;
BEGIN
    SELECT * BULK COLLECT INTO v_users
    FROM users
    WHERE is_active = 1;

    FORALL i IN 1..v_users.COUNT
        UPDATE users
        SET last_login = SYSTIMESTAMP
        WHERE id = v_users(i).id;

    COMMIT;
END;
/
```

## 2. DB2 SQL/PL

### Stored Procedure

```sql
CREATE PROCEDURE create_order (
    IN p_user_id INT,
    IN p_total DECIMAL(10,2),
    OUT p_order_id INT
)
BEGIN
    DECLARE v_status VARCHAR(20) DEFAULT 'pending';

    INSERT INTO orders (user_id, total, status, created_at)
    VALUES (p_user_id, p_total, v_status, CURRENT_TIMESTAMP);

    SET p_order_id = IDENTITY_VAL_LOCAL();
END
```

### MERGE (DB2)

```sql
MERGE INTO inventory AS target
USING (SELECT product_id, quantity FROM staging_inventory) AS source
ON target.product_id = source.product_id
WHEN MATCHED THEN
    UPDATE SET target.quantity = target.quantity + source.quantity
WHEN NOT MATCHED THEN
    INSERT (product_id, quantity) VALUES (source.product_id, source.quantity);
```

## 3. Oracle Partitioning

| Type | Use Case |
|------|----------|
| Range | Time-series data (by month/year) |
| List | Discrete categories (by region/status) |
| Hash | Even distribution for I/O balance |
| Composite | Range + Hash or Range + List |

```sql
CREATE TABLE sales (
    sale_id NUMBER,
    sale_date DATE,
    amount NUMBER(10,2)
) PARTITION BY RANGE (sale_date) (
    PARTITION p2023q1 VALUES LESS THAN (TO_DATE('2023-04-01','YYYY-MM-DD')),
    PARTITION p2023q2 VALUES LESS THAN (TO_DATE('2023-07-01','YYYY-MM-DD')),
    PARTITION p2023q3 VALUES LESS THAN (TO_DATE('2023-10-01','YYYY-MM-DD')),
    PARTITION p2023q4 VALUES LESS THAN (TO_DATE('2024-01-01','YYYY-MM-DD')),
    PARTITION pmax VALUES LESS THAN (MAXVALUE)
);
```

## 4. DB2 Partitioning (Table Partitioning + MDC)

```sql
CREATE TABLE sales (
    sale_id INT,
    sale_date DATE,
    amount DECIMAL(10,2)
) PARTITION BY RANGE (sale_date) (
    STARTING FROM '2023-01-01' ENDING AT '2024-01-01' EVERY 3 MONTHS
)
ORGANIZE BY DIMENSIONS (EXTRACT(YEAR FROM sale_date), EXTRACT(MONTH FROM sale_date));
```

## 5. Performance Tuning

### Oracle Execution Plan

```sql
EXPLAIN PLAN FOR
SELECT * FROM orders WHERE user_id = 42;

SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY);
```

### DB2 Explain

```sql
EXPLAIN PLAN FOR SELECT * FROM orders WHERE user_id = 42;

SELECT * FROM EXPLAIN_INSTANCE;
```

### Index Hints (Oracle)

```sql
SELECT /*+ INDEX(orders idx_orders_user) */ *
FROM orders
WHERE user_id = 42;
```

## 6. JSON Handling

### Oracle JSON

```sql
-- Query JSON column
SELECT id, json_data.name, json_data.address.city
FROM customers,
     JSON_TABLE(
         json_col, '$'
         COLUMNS (
             name VARCHAR2(100) PATH '$.name',
             city VARCHAR2(100) PATH '$.address.city'
         )
     ) json_data
WHERE json_exists(json_col, '$.premium' PASSING 'true' AS "premium");
```

### DB2 JSON

```sql
-- JSON column operations
SELECT id, JSON_VAL(json_col, 'name') AS name
FROM customers
WHERE JSON_EXISTS(json_col, '$.premium');

-- Update JSON
UPDATE customers
SET json_col = JSON_SET(json_col, '$.last_visit', CURRENT_DATE)
WHERE id = 1;
```

## 7. Sequences and Identity

### Oracle

```sql
CREATE SEQUENCE seq_users START WITH 1 INCREMENT BY 1 CACHE 100;

-- Trigger for auto-increment feel
CREATE TRIGGER trg_users_bi
BEFORE INSERT ON users
FOR EACH ROW
BEGIN
    :NEW.id := seq_users.NEXTVAL;
END;
```

### DB2

```sql
-- Identity column
CREATE TABLE users (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(100)
);

-- Sequence
CREATE SEQUENCE seq_orders START WITH 1 INCREMENT BY 1 NO CACHE;
```

## 8. Python Connectivity

### Oracle (cx_Oracle)

```python
import cx_Oracle

dsn = cx_Oracle.makedsn("host", 1521, service_name="ORCL")
with cx_Oracle.connect("user", "password", dsn) as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = :id", {"id": 1})
    row = cursor.fetchone()
```

### DB2 (ibm_db)

```python
import ibm_db

conn_str = (
    "DATABASE=mydb;HOSTNAME=host;PORT=50000;"
    "PROTOCOL=TCPIP;UID=user;PWD=pass;"
)
conn = ibm_db.connect(conn_str, "", "")

stmt = ibm_db.exec_immediate(conn, "SELECT * FROM users FETCH FIRST 10 ROWS ONLY")
result = ibm_db.fetch_both(stmt)
```

## 9. Migration Patterns

### Oracle to PostgreSQL

- Replace `SYSTIMESTAMP` with `CURRENT_TIMESTAMP`.
- Replace `ROWNUM` with `LIMIT`.
- Replace `NVL` with `COALESCE`.
- Replace `DECODE` with `CASE`.
- Use `SERIAL` or `GENERATED ALWAYS AS IDENTITY` instead of sequences + triggers.

### DB2 to PostgreSQL

- Replace `FETCH FIRST n ROWS ONLY` with `LIMIT n`.
- Replace `CURRENT DATE` / `CURRENT TIMESTAMP` with `CURRENT_DATE` / `CURRENT_TIMESTAMP`.
- Replace `IDENTITY_VAL_LOCAL()` with `RETURNING id`.
