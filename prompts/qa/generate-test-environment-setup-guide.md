---
name: Generate Test Environment Setup Guide
version: 1.0.0
author: Mathias Paulenko Echeverz
description: Generate a step-by-step guide for setting up local, staging, and test environments with Docker, test data, and configuration.
tags: [qa, environment, docker, setup, local-development, staging]
role: qa-engineer
model: any
trigger: When the user asks for test environment setup, local testing, Docker compose for testing, or environment configuration.
---

# Generate Test Environment Setup Guide

Generate a step-by-step guide for setting up reproducible test environments.

## Local Environment

### Prerequisites
```bash
# Required software
- Docker Desktop 4.x+
- Node.js 18+ / Python 3.11+
- Git
- Make or Just (task runner)
```

### Quick Start
```bash
# 1. Clone and setup
git clone git@github.com:org/project.git
cd project
cp .env.example .env

# 2. Start dependencies
docker-compose -f docker-compose.test.yml up -d db redis

# 3. Install and run tests
pip install -r requirements-dev.txt
pytest tests/ -m "not slow"
```

### Test Data Seeding
```bash
# Seed with realistic test data
python manage.py seed --count=100 --fixture=fixtures/demo.json
```

## Staging Environment

| Aspect | Configuration |
|--------|---------------|
| Data | Refreshed weekly from prod (anonymized) |
| Scale | 1:10 of production |
| External services | Sandbox APIs (Stripe test, AWS test) |
| CI | Deploys automatically from main branch |
| Monitoring | Same dashboards as prod |

## Configuration Checklist

- [ ] Environment variables documented in `.env.example`
- [ ] No production secrets in test configs
- [ ] Database migrations auto-run on startup
- [ ] Test fixtures version-controlled
- [ ] External service mocks available offline
- [ ] Browser drivers pre-configured (Chrome, Firefox)
- [ ] Mobile emulators configured (Android, iOS)

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| Port conflicts | Another service using 5432 | Change `DB_PORT` in `.env` |
| Tests fail on fresh clone | Missing test data | Run `make seed` |
| E2E tests timeout | Slow machine | Increase `TIMEOUT` in config |
| Docker permission denied | Linux file permissions | `sudo usermod -aG docker $USER` |

## Validation

```bash
# Verify environment is ready
make check-env
# Expected output:
# ✅ Docker running
# ✅ DB accessible
# ✅ Redis accessible
# ✅ Test data seeded
# ✅ All systems go
```
