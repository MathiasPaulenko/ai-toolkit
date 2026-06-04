---
name: Generate CI/CD Quality Gates
version: 1.0.0
author: Mathias Paulenko Echeverz
description: Define CI/CD quality gates for automated testing: code coverage thresholds, static analysis, security scanning, and deployment criteria.
tags: [qa, ci-cd, quality-gates, coverage, sonarqube, pipeline]
role: qa-engineer
model: any
trigger: When the user asks for CI/CD quality gates, pipeline testing, coverage thresholds, or deployment criteria.
---

# Generate CI/CD Quality Gates

Define automated quality gates that must pass before code reaches production.

## Gate Levels

### Gate 1: Commit (Pre-commit hooks)
- [ ] Linting passes (Black, ESLint, Prettier)
- [ ] No secrets in code (gitleaks, truffleHog)
- [ ] Unit tests pass (< 2 min)
- [ ] Coverage does not decrease

### Gate 2: Pull Request
- [ ] All unit tests pass
- [ ] Code coverage ≥ 80% (business logic)
- [ ] SonarQube quality gate passes
- [ ] Security scan (Snyk, Dependabot) — no high/critical
- [ ] Static analysis (bandit, semgrep)
- [ ] Build succeeds (Docker image)

### Gate 3: Integration
- [ ] Integration tests pass
- [ ] Contract tests pass (Pact)
- [ ] API compatibility check
- [ ] Database migration test

### Gate 4: Staging
- [ ] E2E smoke tests pass
- [ ] Performance baseline met (no regression > 10%)
- [ ] Accessibility audit (axe-core)
- [ ] Cross-browser sanity (Chrome, Firefox, Safari)

### Gate 5: Production
- [ ] Canary deployment health checks (5 min)
- [ ] Error rate < 0.1%
- [ ] p95 latency within SLA
- [ ] Rollback ready (blue/green or feature flags)

## Configuration Examples

### GitHub Actions
```yaml
- name: Quality Gate
  run: |
    pytest --cov=src --cov-fail-under=80
    sonar-scanner
    snyk test --severity-threshold=high
```

### GitLab CI
```yaml
quality_gate:
  stage: test
  script:
    - pytest --cov=src
    - sonar-scanner
  coverage: '/TOTAL.*\s+(\d+%)$$/'
  only:
    - merge_requests
```
