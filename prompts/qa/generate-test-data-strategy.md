---
name: Generate Test Data Strategy
version: 1.0.0
author: Mathias Paulenko Echeverz
description: Design a test data strategy covering synthetic generation, masking, subsetting, referential integrity, GDPR compliance, and environment parity.
tags: [test-data, strategy, masking, gdpr, synthetic]
role: qa-lead
model: any
trigger: When the user asks for test data strategy, data masking, synthetic data generation, or test environment data management.
---

# Generate Test Data Strategy

Design a comprehensive strategy for managing test data.

## Data Sources Comparison

| Source | Speed | Realism | Privacy Risk | Best For |
|--------|-------|---------|-------------|----------|
| Production clone | Fast | High | **Critical** | None — too risky |
| Masked production | Medium | High | Low | Regression, performance |
| Synthetic generation | Fast | Medium | None | Unit, integration, new features |
| Subset + referential | Slow | High | Low | Complex relational systems |
| Hand-crafted | Slow | High | None | Edge cases, specific scenarios |

## Strategy Components

### 1. Synthetic Data Generation

```python
# Python with Faker
from faker import Faker
import random

fake = Faker()

def generate_user():
    return {
        "id": fake.uuid4(),
        "email": fake.unique.email(),
        "name": fake.name(),
        "phone": fake.numerify(text='(###) ###-####'),
        "address": fake.address(),
        "registered_at": fake.date_time_between(start_date='-2y'),
        "is_active": random.choice([True, False]),
    }

# Generate 10K users
users = [generate_user() for _ in range(10000)]
```

### 2. Data Masking Rules

| Field | Technique | Example |
|-------|-----------|---------|
| Email | Partial mask | `a***@example.com` |
| SSN | Hash + salt | `***-**-6789` |
| Name | Faker replacement | `John Smith` → `Jane Doe` |
| Address | Generalization | `123 Main St` → `Anytown, USA` |
| Credit Card | Tokenization | `411111******1111` |
| Date of Birth | Shift ± days | `1990-01-15` → `1990-01-22` |

### 3. Referential Integrity

```sql
-- Subset extraction with referential integrity
WITH subset_orders AS (
  SELECT * FROM orders
  WHERE created_at > NOW() - INTERVAL '90 days'
    AND status IN ('completed', 'refunded')
  LIMIT 10000
)
SELECT o.*, c.*, i.*
FROM subset_orders o
JOIN customers c ON o.customer_id = c.id
JOIN order_items i ON i.order_id = o.id;
```

### 4. Environment Parity

| Environment | Data Strategy | Refresh Frequency |
|-------------|-------------|-------------------|
| Local | Synthetic seed + fixtures | Per test run |
| CI | Minimal synthetic dataset | Per build |
| Staging | Masked production subset | Weekly |
| Performance | Full masked production | Monthly |
| UAT | Representative subset | Per release |

## GDPR / Privacy Compliance

- **Article 25**: Data minimization — only collect what's needed
- **Article 32**: Pseudonymization — replace direct identifiers
- **Article 17**: Right to erasure — include cleanup scripts
- **Audit trail**: Log who accessed what test data when

```bash
# Cleanup script for CI
curl -X DELETE http://test-api/cleanup-all-data
# Or database truncate
truncate table orders, customers, sessions restart identity cascade;
```

## Tools

| Tool | Purpose | Language |
|------|---------|----------|
| **Faker** | Synthetic data | Python/JS/PHP |
| **TDK (Tonic)** | Enterprise masking | SaaS |
| **Delphix** | Data virtualization | Enterprise |
| **Synthesized.io** | AI-generated data | Python |
| **Jailer** | Subset extraction | Java |

## Anti-Patterns

| Anti-Pattern | Fix |
|--------------|-----|
| Production data in dev/staging | Use masking or synthesis |
| Hardcoded test data | Use factories/generators |
| No cleanup between tests | Add teardown or use transactions |
| Ignoring referential integrity | Extract subsets with joins |
| Storing PII in repos | Use environment variables/secrets |

## Output

Provide:
1. Data source recommendation per environment
2. Masking rules table for sensitive fields
3. Synthetic data generation script (language-agnostic pseudocode)
4. Refresh schedule
5. Compliance checklist
