# Tools

Scripts, utilities, and auxiliary technical resources.

## Available Tools

| Tool | Purpose |
|------|---------|
| `validate-resource/` | Validate frontmatter, naming, and placeholders across all resources |
| `check-dead-links/` | Scan `.md` files for broken external URLs |
| `export-skills-to-md/` | Concatenate skills into a single markdown bundle |
| `generate-skill-scaffold/` | Interactive scaffold generator for new skills |
| `sync-skills-to-cursor/` | Sync skills to `.cursor/rules/` |
| `sync-skills-to-claude/` | Sync skills to `.claude/agents/` |
| `skills.sh` | Install or inspect skills in the Windsurf skills directory |
| `tests/` | pytest suite for the tools |

## Usage

All Python tools are run via `make`/`just` targets (`make validate`,
`make check-links`, `make export`, `make sync-all`) or directly:

```bash
python tools/validate-resource/validate.py
python tools/check-dead-links/check.py --ignore example.org
```

`skills.sh` is Bash: `./tools/skills.sh [--stats] [target-dir]`.
It auto-detects WSL (`/mnt/c`) vs Git Bash (`/c`) mount styles.

## Convention

- Each tool goes in its own subfolder with a `README.md` explaining usage and installation
- Prefer common languages: Python, Bash, Node.js
- Include `requirements.txt`, `package.json`, or equivalent if applicable
