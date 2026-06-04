---
name: Generate QA Interview Questions
version: 1.0.0
author: Mathias Paulenko Echeverz
description: Generate structured interview questions for QA engineer candidates covering test design, automation, tools, and problem-solving.
tags: [qa, interview, hiring, assessment, career]
role: qa-engineer
model: any
trigger: When the user asks for QA interview questions, hiring assessment, or technical interview preparation.
---

# Generate QA Interview Questions

Generate structured interview questions for QA engineer candidates at different seniority levels.

## Junior QA (0-2 years)

### Test Design
1. "Given a login form with email and password, what test cases would you write?"
2. "What's the difference between smoke and sanity testing?"
3. "Explain equivalence partitioning with an example."

### Tools
4. "Have you used any test management tools? (TestRail, Zephyr, Xray)"
5. "How do you report a bug? What information do you include?"

### Mindset
6. "Why do we need both manual and automated testing?"
7. "What would you do if a developer says 'it works on my machine'?"

## Mid-Level QA (2-5 years)

### Automation
8. "Design a test framework for a REST API. What patterns would you use?"
9. "Your E2E tests are flaky. How do you investigate and fix?"
10. "When would you mock a dependency vs. use the real service?"

### Strategy
11. "We have 2 weeks until release and 200 tests left. What do you do?"
12. "How do you measure test coverage? What are its limitations?"

### Technical
13. "Explain how JWT authentication works and what to test."
14. "What are the risks of testing in production?"

## Senior QA (5+ years)

### Architecture
15. "Design a quality gate strategy for a CI/CD pipeline."
16. "How would you test a distributed system with eventual consistency?"
17. "Explain contract testing and when to use it."

### Leadership
18. "How do you convince a team to invest in test automation?"
19. "Describe a time you improved test efficiency by 50% or more."
20. "How do you handle a release with known, accepted bugs?"

### Deep Technical
21. "How would you test a system that processes 10,000 events/second?"
22. "Design an observability strategy for test environments."
23. "What testing approach would you use for a machine learning model?"

## Practical Exercise

**Take-home:** Given a simple e-commerce checkout flow, write:
- 10 test cases (positive + negative)
- 3 API tests (Python or JavaScript)
- A bug report for one found issue
- Test data generation script

## Scoring Rubric

| Area | Junior | Mid | Senior |
|------|--------|-----|--------|
| Test Design | Basic EP/BVA | Complex scenarios | Risk-based strategy |
| Automation | Can read code | Writes framework | Architect solutions |
| Communication | Reports bugs clearly | Influences decisions | Drives quality culture |
| Problem-solving | Follows checklists | Debugs independently | Prevents categories of bugs |
