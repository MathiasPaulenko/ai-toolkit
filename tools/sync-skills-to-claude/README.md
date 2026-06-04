# sync-skills-to-claude

Copies selected skills to `.claude/agents/` for Claude Dev integration.

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

Creates `.claude/agents/*.md` files that Claude Dev will load as agent context.
