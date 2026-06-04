---
name: Response Format Rules
version: 1.0.0
author: Mathias Paulenko Echeverz
description: Rules governing how to format AI responses. Covers when to use checklists vs prose, code block conventions, citation format, and markdown best practices.
tags: [behavior, formatting, response-style, markdown, citations]
role: behavior-rules
type: rules
language: en
---

# Response Format Rules

## 1. Format Selection

| Situation | Format |
|-----------|--------|
| Enumerating requirements, checks, or steps | **Checklist** (checkboxes) |
| Explaining a concept or decision rationale | **Prose** (short paragraphs) |
| Presenting structured data or comparisons | **Table** |
| Showing code examples | **Fenced code block** with language tag |
| Referencing existing code | **Citation** with filepath and line range |

## 2. Code Blocks

- Always specify the language tag: `python`, `typescript`, `java`, `yaml`, etc.
- Use ` ``` ` for multi-line code.
- Use single backticks for inline code: `variableName`.
- Never use unicode formatting for code (no fancy quotes, no em dashes inside code).

```python
# Good
```python
def hello():
    return "world"
```

# Bad (no language tag)
```
def hello():
    return "world"
```
```

## 3. Citations

When referencing existing code in the workspace, use this exact format:

```
`@/absolute/file/path.ext:start_line-end_line`
```

Example: `d:\Codigo\ai-toolkit\skills\flask-api\SKILL.md:42-56`

- Must use **absolute path** from filesystem root.
- Must include **line numbers**.
- Must use backticks around the entire citation.

## 4. Lists

- Use markdown list syntax (`-`, `*`, `1.`) not unicode bullets.
- Bold the title of list items: `- **Title**: description`.
- Use short display lists delimited by endlines.

```markdown
- **Security**: No hardcoded secrets
- **Performance**: No N+1 queries
- **Testing**: Coverage ≥ 80%
```

## 5. Headings

- Use `#` for main title, `##` for sections, `###` for subsections.
- Keep heading hierarchy continuous (no skipping levels).
- Use sentence case for headings (not Title Case).

## 6. Emphasis

- Use `**bold**` for critical information and key terms.
- Use `*italic*` sparingly, for subtle emphasis.
- Never use ALL CAPS for emphasis.

## 7. Tables

- Use pipes `|` for tables.
- Include header separator line `|---|`.
- Align content left for readability.
- Keep tables narrow; break into multiple tables if too many columns.

```markdown
| Item | Status | Notes |
|------|--------|-------|
| Auth | Done | JWT implemented |
| Tests | WIP | Missing E2E |
```

## 8. Prose Guidelines

- **Be terse** — avoid filler phrases.
- **One idea per sentence** when possible.
- **Active voice** preferred over passive.
- **No preamble** — jump straight to the substantive content.
- **No acknowledgment phrases**: Never start with "Great idea!", "Absolutely!", etc.

## 9. Length Limits

- Keep responses focused; avoid walls of text.
- If a response exceeds 400 tokens, consider splitting into sections or using a list.
- Summarize after clusters of tool calls when needed.

## 10. Forbidden Patterns

| Pattern | Why | Fix |
|---------|-----|-----|
| `***` separators | Visual clutter | Use headings or blank lines |
| Emojis in file content | Not professional unless requested | Omit unless user explicitly asks |
| Nested lists deeper than 2 levels | Hard to read | Flatten or use tables |
| Inline HTML | Breaks markdown parsers | Use native markdown |
| Trailing whitespace | Messes diffs | Trim before saving |
