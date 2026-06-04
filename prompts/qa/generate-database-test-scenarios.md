---
name: Generate Database Test Scenarios
version: 1.0.0
author: Mathias Paulenko Echeverz
description: Generate database testing scenarios for schema validation, data integrity, migrations, indexing, and query performance.
tags: [qa, database, sql, schema, migration, data-integrity]
role: qa-engineer
model: any
trigger: When the user asks for database tests, schema validation, migration testing, or data integrity checks.
---

# Generate Database Test Scenarios

Generate comprehensive database testing scenarios for any relational or NoSQL database.

## 1. Schema Validation

- [ ] All tables/collections exist with correct names
- [ ] Column names, types, and constraints match spec
- [ ] Primary keys defined and unique
- [ ] Foreign keys reference valid tables/columns
- [ ] Indexes exist for frequently queried columns
- [ ] Default values set appropriately
- [ ] CHECK constraints enforce business rules

## 2. Data Integrity

- [ ] Referential integrity (no orphaned records)
- [ ] Unique constraints enforced (emails, usernames)
- [ ] NOT NULL constraints respected
- [ ] Enum values are valid
- [ ] Date ranges are realistic (no future dates for birth dates)
- [ ] No duplicate records
- [ ] Soft delete vs hard delete behavior

## 3. CRUD Operations

```sql
-- Test INSERT with valid data
INSERT INTO users (email, name) VALUES ('test@example.com', 'Alice');

-- Test INSERT violates unique constraint
INSERT INTO users (email, name) VALUES ('test@example.com', 'Bob'); -- Should fail

-- Test UPDATE cascade
UPDATE departments SET id = 99 WHERE id = 1; -- Check FK cascade

-- Test DELETE restrict
DELETE FROM departments WHERE id = 1; -- Should fail if employees exist
```

## 4. Migration Testing

- [ ] Forward migration applies cleanly
- [ ] Rollback migration reverses changes
- [ ] Data preserved during migration
- [ ] Migration is idempotent (safe to rerun)
- [ ] Concurrent migration safety (only one runner)
- [ ] Migration performance on production-size data

## 5. Query Performance

- [ ] Slow query log analysis (< 1s threshold)
- [ ] EXPLAIN plan for critical queries
- [ ] Index usage verification
- [ ] N+1 query detection
- [ ] Connection pool exhaustion test
- [ ] Lock contention under concurrent load

## 6. Backup & Recovery

- [ ] Full backup completes successfully
- [ ] Point-in-time recovery works
- [ ] Backup integrity (checksum validation)
- [ ] Restore to separate environment
- [ ] RTO/RPO compliance verification
