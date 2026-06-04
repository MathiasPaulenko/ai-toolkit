---
name: SonarQube Quality Gates
version: 1.0.0
author: Mathias Paulenko Echeverz
description: SonarQube quality gate configuration, coverage rules, custom profiles, and CI/CD integration for maintaining code quality across projects.
tags: [sonarqube, quality-gates, static-analysis, code-quality, ci-cd, devops]
role: quality-engineer
model: any
trigger: When the user mentions SonarQube, quality gates, code coverage thresholds, static analysis, SonarScanner, or custom quality profiles.
---

# SonarQube Quality Gates

## 1. Core Concepts

| Term | Definition |
|------|------------|
| **Quality Gate** | Pass/fail conditions a project must meet (e.g., coverage ≥ 80%). |
| **Quality Profile** | Set of active rules for a language (e.g., Sonar way for Python). |
| **Issue** | Code smell, bug, or vulnerability detected by a rule. |
| **Measure** | Metric value (coverage, duplication, complexity). |
| **New Code** | Code added/changed since previous analysis (Leak Period). |

## 2. Built-in Quality Gate: Sonar way

Default conditions for overall code and new code:

| Metric | Threshold |
|--------|-----------|
| Coverage | ≥ 80% |
| Duplicated Lines | ≤ 3% |
| Maintainability Rating | A |
| Reliability Rating | A |
| Security Rating | A |
| Security Hotspots Reviewed | 100% |
| Critical Issues | 0 |
| Blocker Issues | 0 |

## 3. Custom Quality Gate

Create a stricter gate for critical projects:

```yaml
# API: POST /api/qualitygates/create
name: "Strict Enterprise Gate"
conditions:
  - metric: coverage
    threshold: "85"
    operator: LT  # fail if less than 85%
  - metric: duplicated_lines_density
    threshold: "2"
    operator: GT
  - metric: critical_violations
    threshold: "0"
    operator: GT
  - metric: security_rating
    threshold: "1"  # A
    operator: GT
  - metric: new_coverage
    threshold: "80"
    operator: LT
  - metric: new_duplicated_lines_density
    threshold: "1"
    operator: GT
```

## 4. SonarScanner Configuration

### `sonar-project.properties`

```properties
# Project identity
sonar.projectKey=my-org:my-service
sonar.projectName=My Service
sonar.projectVersion=1.0.0

# Sources and tests
sonar.sources=src
sonar.tests=tests
sonar.test.inclusions=tests/**/*.py

# Coverage report (pytest-cov)
sonar.python.coverage.reportPaths=coverage.xml

# Exclusions
sonar.exclusions=**/migrations/**,**/vendor/**
sonar.coverage.exclusions=**/config/**,**/tests/**

# Encoding
sonar.sourceEncoding=UTF-8
```

### CI/CD (GitHub Actions)

```yaml
- name: SonarQube Scan
  uses: sonarqube-scan-action@v2
  env:
    SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
    SONAR_HOST_URL: ${{ secrets.SONAR_HOST_URL }}
```

### CI/CD (GitLab CI)

```yaml
sonarqube:
  image: sonarsource/sonar-scanner-cli:latest
  script:
    - sonar-scanner
      -Dsonar.projectKey=$CI_PROJECT_PATH
      -Dsonar.sources=src
      -Dsonar.python.coverage.reportPaths=coverage.xml
```

## 5. Coverage Integration

### Python (pytest + coverage)

```bash
pytest --cov=src --cov-report=xml --cov-fail-under=80
cat coverage.xml  # verify path matches sonar config
```

### Java (JaCoCo)

```xml
<plugin>
  <groupId>org.jacoco</groupId>
  <artifactId>jacoco-maven-plugin</artifactId>
  <version>0.8.11</version>
  <executions>
    <execution>
      <goals><goal>prepare-agent</goal></goals>
    </execution>
    <execution>
      <id>report</id><phase>test</phase>
      <goals><goal>report</goal></goals>
    </execution>
  </executions>
</plugin>
```

## 6. Custom Rules (Python Plugin API)

```python
from python_checkers import Issue, Rule

class NoHardcodedSecretsRule(Rule):
    key = "no-hardcoded-secrets"
    name = "No hardcoded secrets"
    description = "Detects hardcoded API keys and passwords"

    def visit_assign(self, node):
        sensitive_names = {"password", "secret", "token", "api_key"}
        if node.target.id.lower() in sensitive_names:
            if isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
                yield Issue(
                    message=f"Hardcoded secret detected: {node.target.id}",
                    line=node.lineno,
                    severity="BLOCKER",
                )
```

## 7. PR Decoration

Enable pull request analysis to block merges:

```properties
sonar.pullrequest.key=${GITHUB_PR_NUMBER}
sonar.pullrequest.branch=${GITHUB_HEAD_REF}
sonar.pullrequest.base=${GITHUB_BASE_REF}
```

## 8. Best Practices

- Set quality gate as **required check** in GitHub/GitLab.
- Use **new code** conditions to prevent technical debt growth.
- Review **security hotspots** promptly (manual step).
- Track **coverage on new code**, not just overall.
- Exclude generated code (migrations, protobuf, API clients).
- Run analysis on every commit, not just nightly.
