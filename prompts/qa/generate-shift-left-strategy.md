---
name: Generate Shift-Left Strategy
version: 1.0.0
author: Mathias Paulenko Echeverz
description: Design a shift-left testing strategy that embeds quality into the earliest stages of SDLC. Covers TDD, contract testing, linting, pre-commit hooks, and developer ownership.
tags: [shift-left, tdd, quality, sdlc, developer-testing]
role: qa-lead
model: any
trigger: When the user asks about shift-left testing, developer-driven quality, early testing, or embedding QA into development.
---

# Generate Shift-Left Strategy

Design a strategy to move testing earlier in the development lifecycle.

## Shift-Left Pyramid

```
Level 5: Production Monitoring (Observability)
Level 4: E2E / Contract Tests (CI/CD)
Level 3: Integration Tests (PR checks)
Level 2: Unit + Component Tests (Pre-commit / IDE)
Level 1: Static Analysis + Linting (Save / Commit)
Level 0: Requirements Review + Test Design (Story Refinement)
```

## Phase 0: Requirements & Test Design

### Acceptance Criteria as Test Cases

```markdown
## Story: User Login

### Acceptance Criteria
- [ ] Valid credentials redirect to dashboard (< 500ms)
- [ ] Invalid credentials show error without revealing which field
- [ ] Account locked after 5 failed attempts
- [ ] Password reset email sent within 60 seconds

### Test Cases Generated
| ID | Scenario | Type | Owner |
|----|----------|------|-------|
| T1 | Valid login | E2E | QA |
| T2 | Invalid login | Unit | Dev |
| T3 | Rate limiting | Integration | Dev |
| T4 | Email delivery | Contract | Dev |
```

## Phase 1: Static Analysis (Every Save)

### IDE Integration

```json
// .vscode/settings.json
{
  "editor.formatOnSave": true,
  "python.formatting.provider": "ruff",
  "eslint.workingDirectories": ["./frontend"],
  "sonarlint.connectedMode.project": {
    "projectKey": "myapp"
  }
}
```

### Pre-Commit Hooks

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://example.com/ruff-pre-commit
    rev: v0.6.0
    hooks:
      - id: ruff
      - id: ruff-format
  - repo: https://github.com/pre-commit/mirrors-eslint
    rev: v9.0.0
    hooks:
      - id: eslint
  - repo: local
    hooks:
      - id: unit-tests
        name: Run unit tests
        entry: pytest tests/unit -q
        language: system
        pass_filenames: false
```

## Phase 2: Unit & Component (Every Commit)

```python
# Developer writes test with feature
# test_password_validator.py
import pytest
from auth.password import validate_password

@pytest.mark.parametrize("password,expected", [
    ("Short1!", False),    # Too short
    ("nouppercase123!", False),  # No upper
    ("NoNumber!", False),  # No digit
    ("ValidPass123!", True),
])
def test_password_validation(password, expected):
    assert validate_password(password) == expected
```

## Phase 3: Integration (Every PR)

```yaml
# .github/workflows/pr.yml
jobs:
  integration-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Start services
        run: docker-compose -f docker-compose.test.yml up -d
      - name: Run integration tests
        run: pytest tests/integration -v
      - name: Contract tests
        run: pytest tests/contract -v
```

## Phase 4: Contract Testing

```python
# Consumer (frontend)
import requests

def test_api_contract():
    res = requests.get("/api/users/1")
    assert res.status_code == 200
    # Validate schema
    assert "id" in res.json()
    assert "email" in res.json()
    assert isinstance(res.json()["id"], int)
```

## Metrics

| Metric | Before | After | Target |
|--------|--------|-------|--------|
| Bugs found in production | 15/sprint | — | < 3/sprint |
| Time to fix production bug | 3 days | — | < 4 hours |
| Test coverage | 45% | — | > 80% |
| PR cycle time | 5 days | — | < 2 days |
| Developer test ownership | 20% | — | > 70% |

## Anti-Patterns

| Anti-Pattern | Fix |
|--------------|-----|
| QA team writes all tests | Developers own unit + integration |
| Testing after development | Test-first or test-during |
| "We'll add tests later" | Block merge if coverage drops |
| Only happy path tested | Include negative + edge cases |
| Separate QA silo | Embed QA in sprint teams |

## Output

Provide:
1. Current vs desired state assessment
2. Phase-by-phase implementation plan
3. Tooling recommendations per phase
4. Metrics and KPIs to track
5. Change management plan (team training, gradual rollout)
