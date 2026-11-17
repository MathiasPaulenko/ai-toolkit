# Rules

Set of rules to standardize code, reviews, and behavior.

## Structure

- `coding/` — Style, patterns, and code restriction rules
- `review/` — Checklists and criteria for code review
- `behavior/` — Assistant behavior rules (tone, format, language)

## Format

Each rule set is a `.md` file with the standard repository frontmatter
(`name`, `version`, `author`, `description`, `tags`) followed by numbered
or categorized rules.

Example:

```markdown
# Python Coding Rules

## General
1. Use type hints in all public functions
2. Maximum 80 characters per line

## Imports
1. Order: stdlib > third-party > local
2. Avoid circular imports
```
