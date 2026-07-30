---
name: WaveXis Accessibility
version: 1.0.0
author: Mathias Paulenko Echeverz
description: "Accessibility auditing with wavexis. a11y tree snapshots, axe-core audits, node traversal, CI gates for WCAG compliance."
tags: [accessibility, a11y, wcag, axe-core]
trigger: When the user asks about accessibility auditing with wavexis, needs a11y tree snapshots, wants axe-core audits, needs WCAG 2.2 compliance checks, or wants CI accessibility gates.
---

# WaveXis Accessibility

## Description

Accessibility auditing with wavexis — capture accessibility tree snapshots, inspect individual a11y nodes, traverse ancestors, run axe-core audits, map results to WCAG 2.2 criteria, and enforce CI accessibility gates.

## When to Invoke

- Capturing accessibility tree snapshots of a page
- Inspecting individual a11y nodes by ID
- Traversing a11y node ancestors
- Running axe-core accessibility audits
- Mapping audit results to WCAG 2.2 criteria
- Setting up CI accessibility gates
- Checking WCAG compliance for a page

## Prerequisites

- `pip install wavexis[cdp]`
- Chrome or Edge installed
- Basic familiarity with wavexis CLI (see `wavexis-cli-automation` skill)

## a11y Commands

### a11y_tree — Capture accessibility tree

Capture a full accessibility tree snapshot of the current page or a specific node:

```bash
wavexis a11y_tree https://example.com
```

### a11y_tree with selector

```bash
wavexis a11y_tree https://example.com --selector "main"
```

### a11y_tree with output

```bash
wavexis a11y_tree https://example.com --output a11y-tree.json
```

### a11y_tree output format

```json
{
  "nodes": [
    {
      "node_id": 1,
      "role": "WebArea",
      "name": "Example Domain",
      "ignored": false,
      "child_ids": [2, 3, 4]
    },
    {
      "node_id": 2,
      "role": "heading",
      "name": "Example Domain",
      "level": 1,
      "ignored": false,
      "child_ids": []
    },
    {
      "node_id": 3,
      "role": "link",
      "name": "More information...",
      "ignored": false,
      "child_ids": [],
      "focusable": true,
      "url": "https://www.iana.org/domains/example"
    }
  ]
}
```

### a11y_node — Inspect individual node

Inspect a specific accessibility node by its node ID:

```bash
wavexis a11y_node https://example.com --node-id 2
```

### a11y_node output

```json
{
  "node_id": 2,
  "role": "heading",
  "name": "Example Domain",
  "level": 1,
  "ignored": false,
  "ignored_reasons": [],
  "child_ids": [],
  "properties": {
    "level": 1,
    "browserName": "Example Domain"
  }
}
```

### a11y_ancestors — Traverse ancestors

Get the ancestor chain of a specific accessibility node:

```bash
wavexis a11y_ancestors https://example.com --node-id 3
```

### a11y_ancestors output

```json
{
  "ancestors": [
    {
      "node_id": 1,
      "role": "WebArea",
      "name": "Example Domain"
    },
    {
      "node_id": 5,
      "role": "paragraph",
      "name": ""
    },
    {
      "node_id": 3,
      "role": "link",
      "name": "More information..."
    }
  ]
}
```

### a11y command options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--selector` | `str` | None | CSS selector to scope the tree |
| `--node-id` | `int` | None | Node ID for `a11y_node` and `a11y_ancestors` |
| `--output` | `str` | stdout | Output file path |
| `--format` | `str` | `json` | Output format: `json` or `text` |
| `--wait-for` | `str` | None | Wait for selector before capture |
| `--timeout` | `int` | `30000` | Timeout in ms |

## axe Command — axe-core Audits

Run axe-core accessibility audits on a page.

### Basic axe audit

```bash
wavexis axe https://example.com
```

### axe with specific rules

```bash
wavexis axe https://example.com --rules color-contrast,label,image-alt
```

### axe with tags (rule categories)

```bash
wavexis axe https://example.com --tags wcag2a,wcag2aa,wcag21aa
```

### axe with output

```bash
wavexis axe https://example.com --output axe-results.json
```

### axe results format

```json
{
  "passes": [
    {
      "id": "image-alt",
      "impact": null,
      "tags": ["wcag2a", "cat.images"],
      "description": "Images must have alternate text",
      "nodes": [
        {
          "target": ["img.logo"],
          "html": "<img src=\"logo.png\" alt=\"Company Logo\">"
        }
      ]
    }
  ],
  "violations": [
    {
      "id": "color-contrast",
      "impact": "serious",
      "tags": ["wcag2aa", "cat.color"],
      "description": "Elements must have sufficient color contrast",
      "help": "Elements must meet minimum color contrast ratio thresholds",
      "nodes": [
        {
          "target": [".text-muted"],
          "html": "<span class=\"text-muted\">Footer text</span>",
          "failureSummary": "Fix any of the following:\n  Element has insufficient color contrast of 3.2:1"
        }
      ]
    }
  ],
  "incomplete": [
    {
      "id": "color-contrast",
      "impact": "minor",
      "tags": ["wcag2aa"],
      "nodes": []
    }
  ],
  "inapplicable": [
    {
      "id": "audio-caption",
      "impact": null,
      "tags": ["wcag2a"],
      "nodes": []
    }
  ]
}
```

### axe with assert (CI gate)

```bash
wavexis axe https://example.com \
    --tags wcag2a,wcag2aa \
    --assert \
    --output axe-results.json
```

Exits with code 1 if any violations are found.

### axe with impact threshold

```bash
# Only fail on serious or critical violations
wavexis axe https://example.com \
    --impact-threshold serious \
    --assert \
    --output axe-results.json
```

### axe options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--rules` | `str` | all | Comma-separated rule IDs to run |
| `--tags` | `str` | all | Comma-separated tags to filter rules |
| `--exclude` | `str` | None | CSS selector to exclude from audit |
| `--output` | `str` | stdout | Output file path |
| `--format` | `str` | `json` | Output format |
| `--assert` | `flag` | off | Exit 1 if violations found |
| `--impact-threshold` | `str` | `minor` | Minimum impact to fail: `minor`, `moderate`, `serious`, `critical` |
| `--wait-for` | `str` | None | Wait for selector before audit |
| `--timeout` | `int` | `30000` | Timeout in ms |

## Interpreting a11y Tree Results

### Key fields

| Field | Description |
|-------|-------------|
| `node_id` | Unique ID for the node in the tree |
| `role` | ARIA role (e.g., `heading`, `link`, `button`) |
| `name` | Accessible name of the node |
| `ignored` | Whether the node is ignored by assistive tech |
| `ignored_reasons` | Why the node was ignored |
| `child_ids` | Child node IDs |
| `level` | Heading level (for heading roles) |
| `focusable` | Whether the node is focusable |
| `properties` | Additional ARIA properties |

### Common roles

| Role | Description | Common elements |
|------|-------------|-----------------|
| `WebArea` | Root of the a11y tree | `<body>` / document |
| `heading` | Heading with level | `<h1>` - `<h6>` |
| `link` | Hyperlink | `<a>` |
| `button` | Button control | `<button>` |
| `textbox` | Text input | `<input type="text">`, `<textarea>` |
| `image` | Image with alt text | `<img>` |
| `list` | List container | `<ul>`, `<ol>` |
| `listitem` | List item | `<li>` |
| `navigation` | Navigation region | `<nav>` |
| `main` | Main content region | `<main>` |
| `banner` | Banner region | `<header>` |
| `contentinfo` | Content info region | `<footer>` |
| `form` | Form region | `<form>` |
| `combobox` | Combo box | `<select>`, ARIA combobox |
| `checkbox` | Checkbox control | `<input type="checkbox">` |
| `radio` | Radio button | `<input type="radio">` |
| `tab` | Tab in a tab list | ARIA `role="tab"` |
| `dialog` | Dialog or modal | ARIA `role="dialog"` |

### Ignored nodes

Nodes can be ignored for several reasons:

| Reason | Description |
|--------|-------------|
| `notRendered` | Element is not visible (display:none, visibility:hidden) |
| `notVisible` | Element is visually hidden |
| `ariaHidden` | Element has `aria-hidden="true"` |
| `presentational` | Element has a presentational role |
| `empty` | Element has no accessible name or content |

## WCAG 2.2 Criteria Mapping

axe-core results map to WCAG 2.2 criteria via tags. Each violation includes tags like `wcag2a`, `wcag2aa`, `wcag21aa`, `wcag22aa`.

### WCAG levels

| Level | Tag | Meaning |
|-------|-----|---------|
| A | `wcag2a`, `wcag21a`, `wcag22a` | Minimum compliance |
| AA | `wcag2aa`, `wcag21aa`, `wcag22aa` | Standard compliance |
| AAA | `wcag2aaa`, `wcag21aaa` | Enhanced compliance |

### Common axe-core to WCAG mapping

| axe Rule | WCAG Criterion | Level |
|----------|---------------|-------|
| `color-contrast` | 1.4.3 Contrast (Minimum) | AA |
| `image-alt` | 1.1.1 Non-text Content | A |
| `label` | 3.3.2 Labels or Instructions | A |
| `heading-order` | 1.3.1 Info and Relationships | A |
| `tabindex` | 2.4.3 Focus Order | A |
| `landmark-one-main` | 1.3.1 Info and Relationships | A |
| `button-name` | 4.1.2 Name, Role, Value | A |
| `link-name` | 4.1.2 Name, Role, Value | A |
| `html-has-lang` | 3.1.1 Language of Page | A |
| `html-lang-valid` | 3.1.1 Language of Page | A |
| `focus-order-semantics` | 2.4.3 Focus Order | A |
| `target-size` | 2.5.8 Target Size (Minimum) | AA |
| `focus-visible` | 2.4.7 Focus Visible | AA |
| `aria-valid-attr` | 4.1.2 Name, Role, Value | A |
| `aria-required-attr` | 4.1.2 Name, Role, Value | A |

## CI Integration

### Accessibility gate in CI

```bash
wavexis axe https://staging.example.com \
    --tags wcag2a,wcag2aa \
    --impact-threshold serious \
    --assert \
    --output axe-results.json
```

### GitHub Actions integration

```yaml
- name: Accessibility audit
  run: |
    wavexis axe https://staging.example.com \
        --tags wcag2a,wcag2aa,wcag21aa,wcag22aa \
        --impact-threshold moderate \
        --assert \
        --output axe-results.json

- name: Upload results
  if: always()
  uses: actions/upload-artifact@v4
  with:
    name: a11y-results
    path: axe-results.json
```

### Multi-action YAML for a11y audit

```yaml
actions:
  - navigate:
      url: https://example.com
      wait_until: networkidle
  - a11y_tree:
      output: a11y-tree.json
  - axe:
      tags:
        - wcag2a
        - wcag2aa
        - wcag21aa
        - wcag22aa
      impact_threshold: moderate
      output: axe-results.json
  - screenshot:
      full_page: true
```

## Best Practices

- **Audit all WCAG levels** — use `--tags wcag2a,wcag2aa,wcag21aa,wcag22aa` for full coverage.
- **Use `--assert` in CI** — fail builds on accessibility violations.
- **Set impact threshold** — `--impact-threshold serious` to focus on critical issues first.
- **Capture a11y tree** — use `a11y_tree` for debugging specific accessibility issues.
- **Inspect nodes** — use `a11y_node` and `a11y_ancestors` to trace issues to their source.
- **Exclude non-content** — use `--exclude` to skip decorative elements or third-party widgets.
- **Save results** — `--output` for artifacts and trend analysis.
- **Test after changes** — re-run axe after fixing violations to verify.
- **Test dynamic content** — use `--wait-for` for SPAs and dynamic content.
- **Map to WCAG** — use the tags in results to identify which WCAG criteria failed.

## Common Pitfalls

- **Only testing A level** — AA is the standard for most compliance requirements.
- **Ignoring incomplete results** — `incomplete` means axe couldn't determine pass/fail; investigate manually.
- **Excluding too much** — overusing `--exclude` can hide real issues.
- **Not testing keyboard navigation** — axe checks markup, not actual keyboard behavior; test manually.
- **Missing dynamic content** — SPA content loaded after audit won't be checked; use `--wait-for`.
- **Ignoring color contrast** — most common violation; check with `--rules color-contrast`.
- **Not testing forms** — form accessibility is critical; use `--rules label,name,form-field-multiple-labels`.
- **Forgetting `aria-hidden`** — elements with `aria-hidden="true"` should not be focusable.

## References

- `references/wcag-mapping.md` — WCAG 2.2 criteria to a11y result mapping
- `references/axe-core-rules.md` — axe-core rule categories
- `assets/templates/a11y-audit.yml` — Accessibility audit template
- `assets/templates/ci-a11y-gate.yml` — CI accessibility gate template
- [axe-core](https://github.com/dequelabs/axe-core)
- [WCAG 2.2](https://www.w3.org/TR/WCAG22/)
- [WAI-ARIA](https://www.w3.org/TR/wai-aria/)
