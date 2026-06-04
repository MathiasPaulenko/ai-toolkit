# validate-resource

Validates ai-toolkit resources (skills, agents, prompts, rules, workflows) against repository conventions.

## Checks

- Frontmatter YAML is valid and contains required fields
- Folder and file names are kebab-case
- No placeholder text (`TODO`, `Agent Name`, etc.)
- SKILL.md length is within limits (≤ 600 lines)
- Author field is `Mathias Paulenko Echeverz`

## Requirements

```bash
pip install pyyaml
```

## Usage

```bash
# Validate entire repo
python validate.py

# Validate specific resource
python validate.py skills/flask-api

# Validate from repo root
python tools/validate-resource/validate.py
```

## Exit codes

| Code | Meaning |
|------|---------|
| 0 | All resources valid |
| 1 | Validation failed |
