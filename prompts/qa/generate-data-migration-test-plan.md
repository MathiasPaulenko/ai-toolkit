---
name: Generate Data Migration Test Plan
version: 1.0.0
author: Mathias Paulenko Echeverz
description: Generate a data migration test plan covering data integrity, rollback procedures, performance impact, and validation queries.
tags: [qa, data-migration, database, integrity, rollback, etl]
role: qa-engineer
model: any
trigger: When the user asks for data migration testing, ETL testing, database migration validation, or data integrity checks.
---

# Generate Data Migration Test Plan

Generate a comprehensive data migration test plan to ensure data integrity during system migrations, schema changes, or ETL processes.

## Pre-Migration Checks

- [ ] Baseline data snapshot (row counts, checksums)
- [ ] Identify sensitive data (PII, PCI, PHI)
- [ ] Document source-to-target field mapping
- [ ] Estimate migration duration and downtime
- [ ] Validate rollback plan (can we restore in < 1 hour?)

## Migration Validation

### 1. Row Count & Volume
```sql
-- Source
SELECT COUNT(*) FROM source_table;
SELECT COUNT(*) FROM source_table WHERE status = 'active';

-- Target
SELECT COUNT(*) FROM target_table;
SELECT COUNT(*) FROM target_table WHERE status = 'active';
```

### 2. Data Integrity
```sql
-- Checksum comparison
SELECT MD5(CONCAT(col1, col2, col3)) FROM source_table ORDER BY id;
SELECT MD5(CONCAT(col1, col2, col3)) FROM target_table ORDER BY id;

-- Foreign key integrity
SELECT * FROM orders o WHERE NOT EXISTS (
    SELECT 1 FROM customers c WHERE c.id = o.customer_id
);
```

### 3. Field Mapping Accuracy
- [ ] All required fields populated
- [ ] Default values applied correctly
- [ ] Data type conversions accurate (timestamp, decimal, boolean)
- [ ] Enum values mapped correctly
- [ ] No data truncation (string length, precision)

### 4. Business Rules
- [ ] Calculated fields recomputed correctly
- [ ] Status transitions preserved
- [ ] Audit timestamps maintained
- [ ] Soft deletes preserved

## Post-Migration Checks

- [ ] Application reads migrated data correctly
- [ ] Reports produce same results as pre-migration
- [ ] Search/index updated
- [ ] No orphaned records
- [ ] Performance baseline met

## Rollback Verification

```sql
-- Can we restore?
RESTORE DATABASE production FROM backup_pre_migration;
-- Verify restoration succeeded
SELECT COUNT(*) FROM restored_table;
```
