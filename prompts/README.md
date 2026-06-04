# Prompts

Collection of prompts organized by type.

## Structure

- `system/` — System prompts to configure the base model behavior
- `task/` — Prompts for specific tasks (refactor, testing, documentation, etc)
- `templates/` — Parametrizable templates to reuse with variables

## File Convention

Each prompt is a `.md` file with the following format:

```markdown
---
role: system | task | template
description: what it does
model: gpt-4o | claude-sonnet | any
---

Prompt content...
```

Use `{{variable}}` for parametrizable templates.
