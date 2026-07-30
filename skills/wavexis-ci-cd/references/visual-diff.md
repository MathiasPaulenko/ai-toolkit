# Visual Diff — Visual Regression Setup and Baselines

> Guide to visual regression testing with wavexis `visual-diff` command.

## Overview

Visual regression testing compares a page screenshot against a baseline image to detect unintended visual changes. The `visual-diff` command captures a screenshot, compares it pixel-by-pixel, and produces a diff image highlighting changed areas.

## Basic Usage

### Generate a baseline

```bash
wavexis screenshot https://example.com \
    --full-page \
    --output ./baselines/homepage.png
```

### Run visual diff

```bash
wavexis visual-diff https://example.com \
    --baseline ./baselines/homepage.png \
    --output ./diffs/homepage-diff.png \
    --threshold 0.1
```

### Visual diff with assertion

```bash
wavexis visual-diff https://example.com \
    --baseline ./baselines/homepage.png \
    --threshold 0.1 \
    --assert 'diff_percentage <= 0.1' \
    --output ./diffs/homepage-diff.png
```

## Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--baseline` | `str` | required | Path to baseline image |
| `--output` | `str` | stdout | Diff output path |
| `--threshold` | `float` | `0.1` | Per-pixel difference threshold (0-1) |
| `--full-page` | `flag` | off | Full page comparison |
| `--viewport` | `str` | `1920x1080` | Viewport size (WxH) |
| `--selector` | `str` | None | CSS selector to compare specific element |
| `--assert` | `str` | None | Assertion expression |
| `--wait-for` | `str` | None | Wait for selector before screenshot |
| `--timeout` | `int` | `30000` | Timeout in ms |

## Output Format

```json
{
  "diff_percentage": 0.03,
  "pixels_changed": 1245,
  "total_pixels": 41472,
  "baseline_size": "1920x1080",
  "current_size": "1920x1080",
  "status": "PASS"
}
```

### Fail output

```json
{
  "diff_percentage": 0.15,
  "pixels_changed": 6220,
  "total_pixels": 41472,
  "baseline_size": "1920x1080",
  "current_size": "1920x1080",
  "status": "FAIL"
}
```

## Threshold Tuning

### How threshold works

The `--threshold` value (0-1) controls per-pixel sensitivity:

| Threshold | Sensitivity | Use case |
|-----------|-------------|----------|
| `0.01` | Very strict | Pixel-perfect pages (causes flaky CI) |
| `0.05` | Strict | Production pages with minor anti-aliasing |
| `0.1` | Balanced | Recommended starting point |
| `0.2` | Lenient | Pages with dynamic content or ads |
| `0.3` | Very lenient | Pages with heavy dynamic content |

### Diff percentage vs threshold

- `--threshold` controls per-pixel sensitivity.
- `diff_percentage` in output is the ratio of changed pixels to total pixels.
- Assert on `diff_percentage` for CI gates: `--assert 'diff_percentage <= 0.1'`.

## Baseline Management

### Directory structure

```
baselines/
  homepage-desktop.png
  homepage-mobile.png
  product-page-desktop.png
  product-page-mobile.png
  checkout-desktop.png
  checkout-mobile.png
```

### Generating baselines

```bash
# Desktop baseline
wavexis screenshot https://example.com \
    --viewport 1920x1080 \
    --full-page \
    --output ./baselines/homepage-desktop.png

# Mobile baseline
wavexis screenshot https://example.com \
    --viewport 375x812 \
    --full-page \
    --output ./baselines/homepage-mobile.png
```

### Updating baselines

After an intentional UI change:

```bash
# Re-generate baseline
wavexis screenshot https://example.com \
    --viewport 1920x1080 \
    --full-page \
    --output ./baselines/homepage-desktop.png

# Commit the new baseline
git add baselines/homepage-desktop.png
git commit -m "Update homepage baseline after UI redesign"
```

### Baseline best practices

- **Store baselines in git** — version-controlled and reviewable.
- **Separate desktop and mobile** — different viewports produce different screenshots.
- **Name by page and viewport** — `page-viewport.png` convention.
- **Regenerate after approved changes** — don't let baselines go stale.
- **Review baseline diffs in PRs** — visual changes should be reviewed.
- **Use `--selector` for components** — compare specific components, not full pages.

## CI Integration

### GitHub Actions

```yaml
name: Visual Regression

on:
  pull_request:
    branches: [main]

jobs:
  visual:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install wavexis
        run: pip install wavexis[cdp]

      - name: Install Chrome
        run: |
          wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
          sudo sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
          sudo apt-get update && sudo apt-get install -y google-chrome-stable

      - name: Visual diff
        run: |
          wavexis visual-diff https://staging.example.com \
            --baseline ./baselines/homepage-desktop.png \
            --viewport 1920x1080 \
            --threshold 0.1 \
            --assert 'diff_percentage <= 0.1' \
            --output ./diffs/homepage-diff.png

      - name: Upload diff
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: visual-diff
          path: ./diffs/
```

### Multi-page visual regression

```bash
# Run visual diff for multiple pages
for page in homepage product checkout; do
  wavexis visual-diff "https://staging.example.com/${page}" \
    --baseline "./baselines/${page}-desktop.png" \
    --viewport 1920x1080 \
    --threshold 0.1 \
    --assert 'diff_percentage <= 0.1' \
    --output "./diffs/${page}-diff.png" || exit 1
done
```

## Common Issues

### Flaky diffs

| Cause | Solution |
|-------|----------|
| Anti-aliasing differences | Increase `--threshold` to 0.05-0.1 |
| Dynamic content (dates, ads) | Use `--selector` to exclude dynamic areas |
| Font rendering differences | Use consistent Docker images in CI |
| Animation capture timing | Use `--wait-for` to wait for stable state |
| Viewport differences | Always specify `--viewport` explicitly |

### Size mismatch

If baseline and current screenshots have different dimensions:

```json
{
  "diff_percentage": 1.0,
  "pixels_changed": 41472,
  "total_pixels": 41472,
  "baseline_size": "1920x1080",
  "current_size": "1920x900",
  "status": "FAIL",
  "error": "Size mismatch: baseline 1920x1080 vs current 1920x900"
}
```

**Fix**: Ensure the same `--viewport` and `--full-page` settings are used for both baseline and diff.

## References

- [wavexis CLI documentation](https://github.com/MathiasPaulenko/wavexis)
- `references/ci-assertions.md` — Assertion patterns and exit codes
