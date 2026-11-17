# Prompts

Collection of prompts organized by type.

## Structure

- `system/` — System prompts to configure the base model behavior
- `task/` — Prompts for specific tasks (refactor, testing, documentation, etc)
- `qa/` — QA engineering prompts (test generation, strategies, audits)
- `ebooks/` — Prompts for the ebook creation pipeline
- `seo/` — Prompts for SEO audits, analysis, and optimization workflows
- `templates/` — Parametrizable templates to reuse with variables

## File Convention

Each prompt is a `.md` file with YAML frontmatter followed by the prompt body:

```markdown
---
name: Prompt Name
version: 1.0.0
author: Mathias Paulenko Echeverz
description: What it does
tags: [tag1, tag2, tag3]
role: role-identifier
model: gpt-4o | claude-sonnet | any
trigger: When the user asks for...
---

Prompt content...
```

`role`, `model`, and `trigger` are optional metadata. Use `{{variable}}`
for parametrizable templates.
