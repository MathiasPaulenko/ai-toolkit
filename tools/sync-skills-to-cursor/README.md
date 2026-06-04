# sync-skills-to-cursor

Copies selected skills to `.cursor/rules/` for Cursor IDE integration.

## Usage

```bash
# Sync all skills
python sync.py --all

# Sync specific skills
python sync.py flask-api behave-bdd

# List available skills
python sync.py --list
```

## Output

Creates `.cursor/rules/*.md` files that Cursor will load as context rules.
