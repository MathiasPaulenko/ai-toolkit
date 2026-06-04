---
name: Prompt Quality Rules
version: 1.0.0
author: Mathias Paulenko Echeverz
description: Rules for designing, reviewing, and maintaining high-quality LLM prompts. Covers Chain-of-Thought, Few-shot, Role Prompting, output structuring, and anti-patterns.
tags: [prompt-engineering, quality, review, llm, rules]
role: prompt-engineer
type: rules
language: en
---

# Prompt Quality Rules

## 1. Role Prompting

### Rule 1.1: Role Must Be Specific
- The prompt body must describe who the model is, not just a frontmatter tag.
- Include expertise level, domain, and communication style.

```markdown
# Good
You are a senior QA automation engineer with 8 years of experience in web and mobile testing.
Your specialty is designing maintainable test frameworks with Playwright and Appium.
You communicate directly and prioritize test reliability over coverage quantity.

# Bad
You are a helpful assistant.
```

### Rule 1.2: Role Must Set Boundaries
- The role must include what the model should NOT do.

```markdown
# Good
Do not suggest manual testing steps. Only provide automated test code.
Do not use deprecated Selenium APIs. Prefer Playwright or WebdriverIO.

# Bad
Be helpful.
```

## 2. Chain-of-Thought (CoT)

### Rule 2.1: CoT for Complex Tasks
- Any task involving reasoning, math, multi-step logic, or decision-making must include CoT instructions.

```markdown
# Good
Before generating the test plan, think step by step:
1. Identify the highest-risk user journeys
2. Determine which layers need testing (unit, integration, e2e)
3. Estimate effort per layer
4. Select tools based on team expertise
5. Verify the plan covers all critical paths
```

### Rule 2.2: CoT Must Be Structured
- CoT must use numbered steps or named phases, not vague "think carefully."

```markdown
# Bad
Think carefully before answering.

# Good
Analyze the requirement in three phases:
Phase 1 — Decompose the user story into testable statements
Phase 2 — Identify boundaries and dependencies
Phase 3 — Prioritize by business risk
```

## 3. Few-Shot Prompting

### Rule 3.1: Minimum 2 Examples
- Every prompt that generates structured output must include at least 2 input/output examples.

```markdown
# Good
## Example 1 — Happy Path
Input: "User logs in with valid credentials"
Output:
| ID | Scenario | Priority |
|----|----------|----------|
| TC-01 | Valid login | High |

## Example 2 — Edge Case
Input: "User logs in with expired session token"
Output:
| ID | Scenario | Priority |
|----|----------|----------|
| TC-02 | Expired token redirect | High |
```

### Rule 3.2: Examples Must Cover Variation
- Examples must differ in at least one dimension: happy path vs edge case, simple vs complex, valid vs invalid.

## 4. Output Structuring

### Rule 4.1: Output Format Defined Before Task
- The expected output format must be specified before the actual task, not as an afterthought.

```markdown
# Good
## Output Format
Provide a markdown table with columns: ID, Scenario, Steps, Expected, Priority.
Then list automation candidates with recommended tools.

## Task
Given the following requirements, generate test cases...

# Bad
## Task
Generate test cases.

Format them in a table.
```

### Rule 4.2: Delimiters for Code/JSON
- Code blocks and JSON must use fenced delimiters with language tags.

```markdown
# Good
```json
{"test_cases": [...]}
```

# Bad
JSON: {"test_cases": [...]}
```

## 5. Context & Constraints

### Rule 5.1: Constraints Are Measurable
- Use numbers, not adjectives.

```markdown
# Good
- Max 20 lines per test function
- Response time must be under 500ms
- Coverage must exceed 80%

# Bad
- Keep tests short
- Fast response
- Good coverage
```

### Rule 5.2: Anti-Patterns Stated Explicitly
- Every prompt must include at least one "do NOT" instruction.

```markdown
# Good
## Anti-Patterns
- Do not use Thread.sleep for waits
- Do not assert on exact error messages from third-party APIs
- Do not share mutable state between tests
```

## 6. Self-Consistency (Optional)

### Rule 6.1: Use for Critical Outputs
- For code generation, architecture decisions, or high-stakes analysis, request multiple reasoning paths.

```markdown
Generate 3 independent approaches. Compare trade-offs. Select the one with best balance of simplicity and coverage. Justify your choice.
```

## Checklist

- [ ] Role is specific with expertise, tone, and boundaries
- [ ] Context and constraints are explicit and measurable
- [ ] CoT instructions present for reasoning tasks
- [ ] At least 2 few-shot examples with variation
- [ ] Output format defined before the task
- [ ] Anti-patterns stated explicitly
- [ ] No subjective adjectives ("good", "best", "appropriate")
- [ ] Prompt length under 1000 lines
