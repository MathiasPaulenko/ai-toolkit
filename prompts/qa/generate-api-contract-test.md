---
name: Generate API Contract Test
version: 1.0.0
author: Mathias Paulenko Echeverz
description: Generate API contract tests using Pact or JSON Schema to ensure consumer-provider compatibility.
tags: [qa, contract-testing, pact, openapi, api, microservices]
role: qa-engineer
model: any
trigger: When the user asks for contract tests, Pact tests, API schema validation, or consumer-driven contracts.
---

# Generate API Contract Test

Generate consumer-driven contract tests to ensure API compatibility between services.

## Pact (Consumer Test)

```python
import requests
from pact import Consumer, Provider

pact = Consumer('order-service').has_pact_with(Provider('payment-service'))

@pact.given('a valid payment method exists')
@pact.upon_receiving('a request to process payment')
@pact.with_request('POST', '/payments', body={
    'order_id': '123',
    'amount': 99.99,
    'currency': 'USD',
    'method': 'credit_card'
})
@pact.will_respond_with(201, body={
    'payment_id': 'uuid',
    'status': 'approved',
    'transaction_id': 'txn_123'
})
def test_process_payment():
    result = requests.post(f"{pact.uri}/payments", json={
        'order_id': '123',
        'amount': 99.99,
        'currency': 'USD',
        'method': 'credit_card'
    })
    assert result.status_code == 201
    assert result.json()['status'] == 'approved'
```

## Provider Verification

```python
# In payment-service CI
import subprocess

subprocess.run([
    'pact-verifier',
    '--provider', 'payment-service',
    '--pact-broker-base-url', 'https://pact-broker.example.com',
    '--provider-app-version', os.environ['CI_COMMIT_SHA'],
    '--publish-verification-results'
])
```

## JSON Schema Validation

```python
import jsonschema
from jsonschema import validate

schema = {
    "type": "object",
    "properties": {
        "id": {"type": "string", "format": "uuid"},
        "email": {"type": "string", "format": "email"},
        "status": {"enum": ["active", "inactive", "pending"]},
        "created_at": {"type": "string", "format": "date-time"}
    },
    "required": ["id", "email", "status"]
}

def test_response_schema():
    resp = requests.get("/api/users/123")
    validate(instance=resp.json(), schema=schema)
```

## Breakage Prevention

- [ ] Contract tests run on every PR (consumer + provider)
- [ ] Pact Broker webhook triggers provider verification
- [ ] Breaking changes require consumer team approval
- [ ] Contract matrix tracked per environment
