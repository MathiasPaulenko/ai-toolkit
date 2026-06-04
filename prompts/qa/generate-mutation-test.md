---
name: Generate Mutation Test
version: 1.0.0
author: Mathias Paulenko Echeverz
description: Set up mutation testing to validate test suite quality. Introduce code mutations and verify tests catch them. Covers Pitest (Java), Infection (PHP), and stryker-js.
tags: [mutation-testing, pitest, infection, quality, coverage]
role: qa-engineer
model: any
trigger: When the user asks about mutation testing, test quality validation, Pitest, Infection, or verifying test suite effectiveness.
---

# Generate Mutation Test

Mutation testing validates that your tests actually catch bugs.

## How Mutation Testing Works

1. Tool introduces small code mutations (e.g., `==` → `!=`, `+` → `-`)
2. Runs test suite against mutated code
3. If tests fail → mutation is "killed" (good)
4. If tests pass → mutation "survives" (bad — test gap found)

**Mutation Score** = (Killed / Total) × 100  
Target: > 70%

## Pitest (Java)

```xml
<!-- pom.xml -->
<plugin>
  <groupId>org.pitest</groupId>
  <artifactId>pitest-maven</artifactId>
  <version>1.15.0</version>
  <configuration>
    <targetClasses>
      <param>com.example.service.*</param>
    </targetClasses>
    <targetTests>
      <param>com.example.service.*Test</param>
    </targetTests>
    <mutators>
      <mutator>CONDITIONALS_BOUNDARY</mutator>
      <mutator>MATH</mutator>
      <mutator>NEGATE_CONDITIONALS</mutator>
      <mutator>RETURN_VALS</mutator>
      <mutator>VOID_METHOD_CALLS</mutator>
    </mutators>
    <threshold>70</threshold>
    <outputFormats>
      <format>HTML</format>
      <format>XML</format>
    </outputFormats>
  </configuration>
</plugin>
```

```bash
mvn org.pitest:pitest-maven:mutationCoverage
```

## Stryker (JavaScript/TypeScript)

```bash
npm install --save-dev @stryker-mutator/core
npx stryker init
```

```json
// stryker.config.json
{
  "testRunner": "jest",
  "reporters": ["html", "clear-text", "progress"],
  "coverageAnalysis": "perTest",
  "mutate": ["src/**/*.ts", "!src/**/*.spec.ts"],
  "thresholds": {
    "high": 80,
    "low": 60,
    "break": 50
  }
}
```

## Infection (PHP)

```bash
composer require --dev infection/infection
```

```json
// infection.json5
{
  "source": {
    "directories": ["src"]
  },
  "logs": {
    "html": "infection.html",
    "summary": "infection-summary.log"
  },
  "mutators": {
    "@default": true,
    "MethodCallRemoval": false
  },
  "minMsi": 70,
    "minCoveredMsi": 80
}
```

## Mutation Types

| Type | Example | When Survives |
|------|---------|---------------|
| **Conditionals Boundary** | `i > 0` → `i >= 0` | Missing boundary test |
| **Math** | `a + b` → `a - b` | No assertion on calculation result |
| **Negate Conditionals** | `if (x == y)` → `if (x != y)` | Missing both true/false path tests |
| **Return Values** | `return x` → `return null` | No assertion on return value |
| **Void Method Calls** | Remove method call | Side effects not verified |
| **Invert Negatives** | `!valid` → `valid` | Missing negative case test |

## CI Integration

```yaml
# .github/workflows/mutation.yml
- name: Run Mutation Tests
  run: mvn org.pitest:pitest-maven:mutationCoverage
- name: Check Threshold
  run: |
    SCORE=$(grep -oP 'mutationCoverage[^>]*>\K[0-9]+' target/pit-reports/*/index.html)
    if [ "$SCORE" -lt 70 ]; then exit 1; fi
```

## Interpreting Results

- **Killed**: Tests detected the mutation — coverage is real
- **Survived**: Tests didn't catch the mutation — add assertions
- **No Coverage**: No tests run the mutated line — write tests
- **Timed Out**: Mutation caused infinite loop — investigate
- **Ignored**: Equivalent mutation (no semantic change) — acceptable

## Anti-Patterns

| Anti-Pattern | Fix |
|--------------|-----|
| Targeting only simple mutators | Use full mutator set for thoroughness |
| Ignoring equivalent mutations | Document known equivalents |
| Running on every commit (slow) | Run nightly or on PR to main |
| No threshold enforcement | Set `--threshold` in CI to block low scores |

## Output

Provide:
1. Tool recommendation based on language
2. Configuration file
3. CI integration command
4. Threshold recommendations
5. How to address survived mutations
