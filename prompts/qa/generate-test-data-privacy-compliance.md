---
name: Generate Test Data Privacy Compliance
version: 1.0.0
author: Mathias Paulenko Echeverz
description: Ensure test data complies with GDPR, HIPAA, and PCI-DSS. Generate synthetic data, anonymization strategies, and compliance checklists.
tags: [qa, privacy, gdpr, hipaa, pci, compliance, synthetic-data]
role: qa-engineer
model: any
trigger: When the user asks for test data privacy, GDPR compliance, data anonymization, or synthetic data generation.
---

# Generate Test Data Privacy Compliance

Ensure test data complies with privacy regulations (GDPR, HIPAA, PCI-DSS) while remaining useful for testing.

## Regulation Requirements

| Regulation | Key Rule | Test Data Impact |
|------------|----------|------------------|
| **GDPR** | No production PII in non-prod | Anonymize or synthetic |
| **HIPAA** | PHI only in secure environments | De-identify (Safe Harbor method) |
| **PCI-DSS** | No real card data in test | Use test PANs from card brands |
| **CCPA** | Consumer data protection | Same as GDPR |

## Anonymization Techniques

### 1. Substitution
Replace real values with fake ones while maintaining referential integrity:
```python
from faker import Faker
fake = Faker()

# Replace emails but keep uniqueness
email_map = {real: fake.email() for real in unique_emails}
```

### 2. Shuffling
Shuffle values within a column (breaks individual linkage):
```python
df['phone'] = df['phone'].sample(frac=1).reset_index(drop=True)
```

### 3. Masking
Partially obscure data:
```python
# Email: a***@example.com
# Card: ****-****-****-1234
```

### 4. Nullification
Remove sensitive fields entirely:
```python
df.drop(columns=['ssn', 'biometric_data'], inplace=True)
```

### 5. Synthetic Generation
Generate completely fake but realistic data:
```python
from faker import Faker
fake = Faker()

synthetic_users = [
    {
        "name": fake.name(),
        "email": fake.email(),
        "address": fake.address(),
        "dob": fake.date_of_birth(minimum_age=18, maximum_age=90)
    }
    for _ in range(1000)
]
```

## Compliance Checklist

- [ ] No production PII in test environments
- [ ] Test credentials don't use real user passwords
- [ ] Logs don't contain tokens, session IDs, or PII
- [ ] Database dumps are encrypted at rest
- [ ] Test data generation is reproducible (fixed seed)
- [ ] Anonymization is irreversible (can't recover original)
- [ ] Data retention policy for test environments (auto-delete after 30 days)

## Verification Tests

```python
def test_no_pii_in_test_data():
    forbidden_patterns = [
        r'\b\d{3}-\d{2}-\d{4}\b',  # SSN
        r'\b4[0-9]{12}(?:[0-9]{3})?\b',  # Visa
    ]
    for pattern in forbidden_patterns:
        assert not re.search(pattern, test_data_dump)
```
