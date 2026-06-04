# generate-skill-scaffold

Interactive CLI to bootstrap a new skill from the template.

## Usage

```bash
# Interactive mode
python generate.py

# Non-interactive mode
python generate.py --name my-skill --description "A great skill"

# See all options
python generate.py --help
```

## Options

| Option | Description |
|--------|-------------|
| `--name` | Skill name (auto kebab-cased) |
| `--description` | One-line description |
| `--tags` | Comma-separated tags |
| `--role` | Primary role identifier |
| `--trigger` | Trigger condition |

## Output

Creates:
```
skills/<skill-name>/
  SKILL.md              # Copied from template
  references/            # Empty folder
  assets/                # Empty folder
```
