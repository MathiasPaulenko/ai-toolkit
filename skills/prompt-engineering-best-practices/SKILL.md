---
name: prompt-engineering-best-practices
version: 1.0.0
author: Mathias Paulenko Echeverz
description: "Best practices for designing high-quality prompts: Chain-of-Thought, Few-shot, Role Prompting, Self-Consistency, and output structuring. Apply to system, task, and template prompts."
tags: [prompt-engineering, llm, cot, few-shot, role-prompting]
role: prompt-engineer
---

# Prompt Engineering Best Practices

Invoke when creating, reviewing, or improving prompts for LLMs. Ensures consistency, accuracy, and reliability across all prompt types.

## The Six Pillars

| Pillar | Purpose | When to Use |
|--------|---------|-------------|
| **Role Prompting** | Establish expertise, tone, constraints | Every prompt |
| **Context & Constraints** | Narrow scope, prevent hallucination | Every prompt |
| **Chain-of-Thought (CoT)** | Improve reasoning on complex tasks | Math, logic, multi-step decisions |
| **Few-Shot Prompting** | Teach output format by example | Structured outputs, creative writing, code |
| **Self-Consistency** | Reduce randomness, increase reliability | Critical decisions, code generation |
| **Output Structuring** | Guarantee parseable, consistent format | APIs, tables, JSON, checklists |

## 1. Role Prompting

Define who the model is and what expertise it brings.

### Template

```markdown
You are a [role] with [X] years of experience in [domain].
Your specialty is [specific area].
You communicate in [tone] and prioritize [values].
```

### Good

```markdown
You are a senior QA automation engineer with 8 years of experience in web and mobile testing.
Your specialty is designing maintainable test frameworks with Playwright and Appium.
You communicate directly and prioritize test reliability over coverage quantity.
```

### Bad

```markdown
You are a QA engineer.
```

### Anti-Patterns

| Bad | Good |
|-----|------|
| "Be helpful" | "You are a security auditor who flags every hardcoded secret" |
| "Write good code" | "You write production Python following PEP 8 and type hints" |
| "Answer questions" | "You answer as a staff engineer who explains trade-offs" |

## 2. Context & Constraints

Provide the model with boundaries before the task.

```markdown
## Context
- Tech stack: Python 3.11, FastAPI, PostgreSQL, pytest
- Team size: 5 developers, 1 QA
- CI/CD: GitHub Actions with 10-minute timeout

## Constraints
- Max 50 lines per function
- Use `async`/`await` for I/O
- No external dependencies beyond `requirements.txt`
```

## 3. Chain-of-Thought (CoT)

For reasoning tasks, instruct the model to think step by step before answering.

### Zero-Shot CoT

```markdown
Before answering, think step by step:
1. Identify the problem type
2. Break it into sub-problems
3. Solve each sub-problem
4. Verify the solution against constraints
5. Provide the final answer
```

### Few-Shot CoT

```markdown
Q: A store has 15 apples. They sell 7, then receive 12 more. How many apples?
Let's think step by step.
Step 1: Start with 15 apples.
Step 2: Subtract 7 sold: 15 - 7 = 8.
Step 3: Add 12 received: 8 + 12 = 20.
Answer: 20 apples.

Q: A test suite has 120 tests. 30% are flaky. After fixing 60% of flaky tests, how many flaky remain?
Let's think step by step.
```

## 4. Few-Shot Prompting

Provide input/output pairs to teach the model the desired format.

### Template

```markdown
## Example 1
Input: [user input]
Output:
```
[desired output]
```

## Example 2
Input: [user input]
Output:
```
[desired output]
```

## Task
Input: [actual user input]
Output:
```

### Few-Shot with Reasoning

```markdown
## Example 1 â€” Test Case Generation
Requirement: "Users can log in with email and password."
Reasoning: This is a happy-path authentication test. Need valid credentials, login action, and dashboard assertion.
Output:
| ID | Scenario | Steps | Expected |
|----|----------|-------|----------|
| TC-01 | Valid login | 1. Enter email 2. Enter password 3. Click Login | Dashboard loads |

## Example 2 â€” Edge Case
Requirement: "Users can log in with email and password."
Reasoning: This tests the boundary of empty password field, which should trigger validation before API call.
Output:
| ID | Scenario | Steps | Expected |
|----|----------|-------|----------|
| TC-02 | Empty password | 1. Enter email 2. Leave password blank 3. Click Login | Inline validation error "Password is required" |
```

## 5. Self-Consistency

Generate multiple reasoning paths and select the most consistent answer.

```markdown
Generate 3 independent answers to this question.
For each answer, show your reasoning.
Then vote: which answer appears most frequently and is best supported?
Provide the consensus answer as the final output.
```

## 6. Output Structuring

Use delimiters, schemas, and formats to guarantee consistent output.

```markdown
## Output Format
Respond ONLY in the following markdown structure:

### Analysis
[Brief analysis in 1-2 sentences]

### Recommendation
[Clear recommendation]

### Rationale
[3 bullet points max]

### Confidence
[High / Medium / Low] with brief justification
```

### JSON Mode

```markdown
Respond with valid JSON only, no markdown, no explanations:
{
  "test_cases": [
    {
      "id": "string",
      "scenario": "string",
      "steps": ["string"],
      "expected": "string",
      "priority": "High|Medium|Low"
    }
  ],
  "risks": ["string"],
  "automation_candidates": ["string"]
}
```

## Prompt Quality Checklist

- [ ] Role is specific (not generic "assistant")
- [ ] Context and constraints are explicit
- [ ] Task is broken into clear steps (CoT for complex tasks)
- [ ] Few-shot examples cover happy path + edge cases
- [ ] Output format is defined with delimiters
- [ ] Anti-patterns or "what NOT to do" are stated
- [ ] Length is under 1000 lines (prefer 300-500)
- [ ] No ambiguous terms ("good", "best", "appropriate")

## Common Anti-Patterns

| Anti-Pattern | Why It Fails | Fix |
|--------------|--------------|-----|
| "Write a good test" | Subjective, no criteria | "Write a pytest test with Arrange-Act-Assert, max 20 lines, using fixtures for DB setup" |
| No output format | Inconsistent structure | Define markdown table or JSON schema |
| No examples | Model guesses format | Provide 2-3 input/output pairs |
| Vague role | Generic tone, no expertise | "You are a senior SRE with Kubernetes in production" |
| No constraints | Hallucination, scope creep | "Use only standard library. No third-party packages." |
