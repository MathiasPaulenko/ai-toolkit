# check-dead-links

Scans all `.md` files for broken external URLs via HEAD requests.

## Usage

```bash
# Check entire repo
python check.py

# Check specific directory
python check.py docs/

# Custom timeout
python check.py --timeout 10

# Ignore patterns
python check.py --ignore example.com --ignore localhost
```

## Options

| Option | Description | Default |
|--------|-------------|---------|
| `--timeout` | Request timeout (seconds) | `10` |
| `--ignore` | URL patterns to skip | `localhost`, `127.0.0.1` |

## Exit codes

| Code | Meaning |
|------|---------|
| 0 | No dead links |
| 1 | Dead links found |
