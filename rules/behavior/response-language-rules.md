---
name: Response Language Rules
version: 1.0.0
author: Mathias Paulenko Echeverz
description: Rules enforcing English-only responses across all interactions.
tags: [behavior, english, language, consistency]
role: behavior-rules
type: rules
language: en
---

# Response Language Rules

## 1. English Only

All responses must be in **English** regardless of the user's input language.

## 2. Technical Terms

- Keep **technical terms** in English: `function`, `class`, `repository`, `endpoint`, `middleware`.
- Do not translate: `pull request`, `merge`, `commit`, `branch`, `pipeline`, `deployment`.
- Explanations, instructions, summaries, and non-technical prose must also be in English.

## 3. Code Examples

All code comments, variable names, and documentation must be in English.

```markdown
# Good
Use `async/await` instead of callbacks to handle asynchronous operations.

# Bad
Mixing English code with non-English comments or variable names.
```

## 4. Consistency Within a Response

- Use **English exclusively** per response.
- Do not switch languages mid-paragraph.
- If the user writes in another language, still respond in English.

## 5. Resource References

When referencing this repository's resources (skills, agents, prompts), use their English names and descriptions as documented.

## 6. Fallback

If uncertain about the user's language preference, default to **English**.
