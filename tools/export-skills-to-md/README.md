# export-skills-to-md

Concatenates selected skills into a single markdown file for manual context pasting.

## Usage

```bash
# Export all skills
python export.py --all --output skills-bundle.md

# Export specific skills
python export.py flask-api behave-bdd --output my-skills.md

# List available skills
python export.py --list
```

## Options

| Option | Description | Default |
|--------|-------------|---------|
| `--output` / `-o` | Output file path | `skills-bundle.md` |
| `--title` | Bundle title | `Skills Bundle` |
| `--all` | Export all skills | — |
