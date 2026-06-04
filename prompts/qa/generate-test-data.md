---
name: Generate Test Data
version: 1.0.0
author: Mathias Paulenko Echeverz
description: Generate realistic, boundary, and edge case test data for any domain. Covers valid/invalid inputs, locale variations, and GDPR-compliant data.
tags: [qa, test-data, fixtures, faker, data-generation]
role: qa-engineer
model: any
trigger: When the user asks for test data, sample data, fixtures, or mock data generation.
---

# Generate Test Data

Generate comprehensive test datasets for any domain or schema.

## Data Categories

### 1. Valid Data (Happy Path)
- Realistic values for each field type
- Locale variations (US, EU, LATAM, APAC)
- Maximum length but valid strings

### 2. Boundary Values
- Empty string, single character
- Max length - 1, max length, max length + 1
- Minimum numeric, zero, negative, maximum
- Date: epoch, today, max date

### 3. Invalid / Error Data
- Wrong type (number in string field)
- Special characters (`<script>`, SQL fragments)
- Unicode edge cases (emoji, RTL, Zalgo)
- Whitespace only, null, undefined

### 4. Security-Focused
- SQL injection strings
- XSS payloads
- Path traversal (`../../etc/passwd`)
- Command injection (`; rm -rf /`)

### 5. Compliance
- GDPR: pseudonymized PII
- PCI: masked credit cards
- HIPAA: synthetic medical records

## Output Formats

### Python (Faker + Factory Boy)
```python
from faker import Faker
fake = Faker()

def generate_user(valid=True):
    if valid:
        return {
            "email": fake.email(),
            "name": fake.name(),
            "age": fake.random_int(18, 99),
            "country": fake.country_code()
        }
    return {
        "email": "invalid",  # Missing @
        "name": "",          # Empty
        "age": -5,           # Negative
        "country": "XX"      # Invalid code
    }
```

### SQL INSERT statements
### CSV for data loading
### JSON for API payloads
