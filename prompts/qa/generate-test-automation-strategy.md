---
name: Generate Test Automation Strategy
version: 1.0.0
author: Mathias Paulenko Echeverz
description: Create a test automation strategy covering tool selection, test pyramid, CI integration, maintenance, and ROI analysis.
tags: [qa, automation, test-strategy, pyramid, roi, tooling]
role: qa-engineer
model: any
trigger: When the user asks for test automation strategy, automation framework, or test pyramid design.
---

# Generate Test Automation Strategy

Create a comprehensive test automation strategy for a project or team.

## 1. Current State Assessment

| Area | Questions |
|------|-----------|
| Coverage | What's manual vs automated? |
| Flakiness | % of flaky tests? Root causes? |
| Speed | How long does the full suite take? |
| Maintenance | Hours/week spent fixing tests? |
| Tools | Current stack, pain points |

## 2. Test Pyramid

```
       /\
      /  \  E2E (10%)  — Playwright, Cypress
     /    \             — Critical user journeys
    /------\  Integration (30%)  — API tests, DB tests
   /        \                  — Service boundaries
  /----------\  Unit (60%)  — pytest, Jest, JUnit
 /            \            — Business logic, utilities
/--------------\
```

## 3. Tool Selection Matrix

| Layer | Python | JavaScript | Java | Mobile |
|-------|--------|------------|------|--------|
| Unit | pytest | Jest/Vitest | JUnit | XCTest/JUnit |
| API | requests + pytest | supertest | RestAssured | — |
| E2E | Playwright | Playwright | Selenium | Appium |
| Contract | pact-python | Pact JS | Pact JVM | — |
| Perf | locust | k6 | JMeter | — |

## 4. CI Integration Strategy

- **Parallel execution**: Shard test suites across workers
- **Test tagging**: `@smoke`, `@regression`, `@flaky`
- **Smart selection**: Only run tests affected by changes
- **Artifacts**: Screenshots, videos, logs on failure
- **Notifications**: Slack/Teams on failure

## 5. Maintenance Plan

- Review flaky tests weekly (goal: < 1% flakiness)
- Archive obsolete tests monthly
- Update selectors when UI changes
- Mock external services to reduce brittleness
- Page Object Model for UI tests

## 6. ROI Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Automation coverage | 80% of testable features | Test case inventory |
| Defect escape rate | < 5% to production | Post-release bugs |
| Test execution time | < 30 min for PR gate | CI pipeline duration |
| Manual regression effort | -50% vs baseline | QA hours per release |
