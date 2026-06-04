---
name: Onboard New Project
version: 1.0.0
author: Mathias Paulenko Echeverz
description: New project setup workflow. Covers repository structure, CI/CD configuration, linting, testing framework, documentation, and team onboarding.
tags: [workflow, project-setup, onboarding, repo-structure, ci-cd, linting, testing]
role: tech-lead
---

# Onboard New Project

## 1. Repository Setup

### Initialize Repository

```bash
git clone https://github.com/org/project-template.git my-project
cd my-project
rm -rf .git
git init
git remote add origin git@github.com:org/my-project.git
```

### Standard Structure

```
my-project/
  src/                     # Source code
  tests/                   # Test files
  docs/                    # Documentation
  .github/                 # GitHub-specific configs
  scripts/                 # Automation scripts
  .gitignore
  README.md
  LICENSE
  CONTRIBUTING.md
```

## 2. README Template

```markdown
# Project Name

One-line description.

## Getting Started

### Prerequisites
- Python 3.11+
- Docker (optional)

### Installation
\`\`\`bash
pip install -r requirements.txt
\`\`\`

### Running Tests
\`\`\`bash
pytest
\`\`\`

## Architecture
Brief architecture overview.

## Contributing
See [CONTRIBUTING.md](CONTRIBUTING.md).
```

## 3. CI/CD Configuration

### GitHub Actions

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.9", "3.10", "3.11"]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
      - run: pip install -r requirements.txt
      - run: pytest --cov=src --cov-report=xml
```

### Branch Protection

- Require pull request reviews (1 approver).
- Require status checks to pass (CI).
- Require branches to be up to date.
- Restrict pushes to maintainers.

## 4. Linting and Formatting

### Python

```bash
pip install black isort ruff pre-commit
pre-commit install
```

### JavaScript / TypeScript

```bash
npm install -D eslint prettier @typescript-eslint/parser
npx eslint --init
```

## 5. Testing Framework

### Python

```bash
pip install pytest pytest-cov
pytest
```

### Java

```xml
<!-- pom.xml -->
<dependency>
  <groupId>org.junit.jupiter</groupId>
  <artifactId>junit-jupiter</artifactId>
  <scope>test</scope>
</dependency>
```

## 6. Documentation

- Add `docs/` folder with architecture decision records (ADRs).
- Set up MkDocs or Sphinx for API documentation.
- Include architecture diagrams (PlantUML or Mermaid).

## 7. Environment Configuration

```bash
# .env.example (no secrets)
DATABASE_URL=postgresql://localhost:5432/mydb
REDIS_URL=redis://localhost:6379/0
LOG_LEVEL=info
```

## 8. Team Onboarding Checklist

- [ ] Clone repo and run tests locally.
- [ ] Set up IDE with linting (ESLint, Black).
- [ ] Read architecture docs and ADRs.
- [ ] Join team Slack/Discord channel.
- [ ] Get access to staging environment.
- [ ] Review coding standards (`rules/coding/`).
