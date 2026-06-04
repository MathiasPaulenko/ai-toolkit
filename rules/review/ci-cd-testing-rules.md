---
name: CI/CD Testing Rules
version: 1.0.0
author: Mathias Paulenko Echeverz
description: Rules for integrating testing into CI/CD pipelines: parallel execution, artifact management, flaky test handling, coverage gates, and deployment validation.
tags: [ci-cd, pipeline, testing, automation, rules]
role: qa-automation-engineer
type: rules
language: en
---

# CI/CD Testing Rules

## 1. Pipeline Structure

### Rule 1.1: Fast Feedback First
- Lint and unit tests must run in under 5 minutes.
- Integration tests should not exceed 15 minutes.
- E2E tests run nightly or on-demand, not on every PR.

```yaml
# Pipeline stages
stages:
  - lint          # < 2 min
  - unit          # < 5 min
  - integration   # < 15 min
  - build
  - e2e           # Nightly only
  - deploy
```

### Rule 1.2: Parallelize Where Possible
- Run tests by file or by tag in parallel workers.
- Use matrix builds for multiple OS/browser combinations.

```yaml
strategy:
  matrix:
    browser: [chrome, firefox, safari]
    os: [ubuntu-latest, windows-latest]
```

## 2. Test Gates

### Rule 2.1: Coverage Gate
- PRs must not reduce test coverage.
- Block merge if coverage drops by > 1%.

```yaml
- name: Check coverage
  run: |
    COVERAGE=$(cat coverage/lcov-report/index.html | grep -oP '\d+(?=%)')
    if [ "$COVERAGE" -lt 80 ]; then exit 1; fi
```

### Rule 2.2: No Flaky Tests in CI
- Flaky tests must be quarantined within 24 hours.
- Track flaky rate; alarm if > 2%.

```yaml
# Retry flaky tests up to 2 times, but flag them
- run: pytest --reruns 2 --reruns-delay 1
- run: python scripts/report_flaky.py
```

## 3. Artifacts & Reporting

### Rule 3.1: Upload on Failure Only
- Screenshots, videos, and traces uploaded only when tests fail.
- Retain artifacts for 7-14 days, not indefinitely.

```yaml
- uses: actions/upload-artifact@v4
  if: failure()
  with:
    name: test-artifacts
    path: |
      screenshots/
      videos/
      traces/
    retention-days: 14
```

### Rule 3.2: Publish Reports Accessibly
- HTML reports published to GitHub Pages or S3 for easy review.
- Slack/Teams notification with direct link to report.

## 4. Environment Management

### Rule 4.1: Isolated Test Environments
- Each PR gets its own ephemeral environment.
- Clean up environments automatically after PR merge.

```bash
# Spin up
docker-compose -f docker-compose.test.yml -p pr-$PR_NUMBER up -d

# Tear down
docker-compose -f docker-compose.test.yml -p pr-$PR_NUMBER down -v
```

### Rule 4.2: Test Data Seeding
- Seed databases with deterministic fixtures before test run.
- Never use production data in CI.

```bash
# Seed script
python manage.py loaddata fixtures/test-data.json
```

## 5. Deployment Validation

### Rule 5.1: Smoke Tests Post-Deploy
- After every deployment, run smoke tests against the new environment.
- If smoke tests fail, trigger automatic rollback.

```yaml
- run: pytest tests/smoke -v
- if: failure()
  run: kubectl rollout undo deployment/app
```

### Rule 5.2: Canary Health Checks
- Before promoting canary to 100%, verify error rate and latency.
- Automatic rollback on threshold breach.

```yaml
- run: ./scripts/check_canary.sh --error-threshold 0.02 --latency-threshold 500
```

## 6. Secrets & Security

### Rule 6.1: No Secrets in Test Code
- API keys, passwords, and tokens injected via CI secrets.
- Use dedicated test accounts, not production credentials.

```yaml
env:
  TEST_API_KEY: ${{ secrets.TEST_API_KEY }}
  TEST_USER_PASSWORD: ${{ secrets.TEST_USER_PASSWORD }}
```

### Rule 6.2: Scan Test Dependencies
- Test libraries must be scanned for CVEs.
- Pin versions to avoid supply chain attacks.

```bash
npm audit --audit-level=moderate
```

## 7. Maintenance

### Rule 7.1: Monitor Pipeline Health
- Track pipeline duration, failure rate, and flaky test rate weekly.
- Investigate if pipeline duration increases by > 20%.

### Rule 7.2: Retire Obsolete Tests
- Delete tests for deprecated features.
- Archive old test suites to reduce noise.

## Checklist

- [ ] Unit tests run in < 5 minutes
- [ ] Coverage gate blocks merge if dropping
- [ ] Artifacts uploaded only on failure
- [ ] Ephemeral environments per PR
- [ ] Smoke tests run post-deploy
- [ ] No secrets in test code
- [ ] Flaky tests quarantined within 24h
- [ ] Pipeline metrics reviewed weekly
