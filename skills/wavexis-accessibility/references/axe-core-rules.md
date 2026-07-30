# axe-core Rule Categories

> Complete reference of axe-core rule categories and commonly used rules.

## Rule Categories

axe-core organizes rules into categories using tags:

| Tag | Category | Description |
|-----|----------|-------------|
| `cat.aria` | ARIA | ARIA attribute and role validation |
| `cat.color` | Color | Color contrast and usage |
| `cat.forms` | Forms | Form labels, inputs, and validation |
| `cat.keyboard` | Keyboard | Keyboard accessibility |
| `cat.language` | Language | Language and reading order |
| `cat.name-role-value` | Name Role Value | Element naming and roles |
| `cat.parsing` | Parsing | HTML parsing and validity |
| `cat.semantics` | Semantics | Semantic HTML and structure |
| `cat.sensory-and-visual-cues` | Sensory | Visual-only indicators |
| `cat.structure` | Structure | Document structure and headings |
| `cat.tables` | Tables | Table accessibility |
| `cat.text` | Text | Text alternatives and content |
| `cat.time` | Time | Time-based media and controls |
| `cat.images` | Images | Image alt text and descriptions |
| `cat.links` | Links | Link accessibility |
| `cat.lists` | Lists | List structure and semantics |

## WCAG Tags

| Tag | WCAG Version | Level |
|-----|-------------|-------|
| `wcag2a` | WCAG 2.0 | A |
| `wcag2aa` | WCAG 2.0 | AA |
| `wcag2aaa` | WCAG 2.0 | AAA |
| `wcag21a` | WCAG 2.1 | A |
| `wcag21aa` | WCAG 2.1 | AA |
| `wcag21aaa` | WCAG 2.1 | AAA |
| `wcag22a` | WCAG 2.2 | A |
| `wcag22aa` | WCAG 2.2 | AA |

## Best Practice Tags

| Tag | Description |
|-----|-------------|
| `best-practice` | Not WCAG-required but recommended |
| `ACT` | Accessibility Conformance Testing rules |
| `section508` | US Section 508 compliance |
| `section508.*.a` | Section 508 paragraph A |
| `section508.*.b` | Section 508 paragraph B |

## Experimental Tags

| Tag | Description |
|-----|-------------|
| `experimental` | Rules that may change |
| `review-item` | Items needing manual review |

## Common Rules by Category

### ARIA Rules

| Rule ID | Impact | Description |
|---------|--------|-------------|
| `aria-allowed-attr` | critical | ARIA attributes must match role |
| `aria-allowed-role` | minor | Role must be allowed on element |
| `aria-command-name` | serious | ARIA commands must have name |
| `aria-hidden-body` | critical | Body must not be `aria-hidden` |
| `aria-hidden-focus` | serious | `aria-hidden` elements must not be focusable |
| `aria-input-field-name` | serious | ARIA input fields must have name |
| `aria-required-attr` | critical | Required ARIA attributes present |
| `aria-required-children` | critical | Required ARIA children present |
| `aria-required-parent` | critical | Required ARIA parent present |
| `aria-roles` | critical | ARIA roles must be valid |
| `aria-toggle-field-name` | serious | Toggle fields must have name |
| `aria-valid-attr` | critical | ARIA attributes must be valid |
| `aria-valid-attr-value` | critical | ARIA attribute values must be valid |

### Color Rules

| Rule ID | Impact | Description |
|---------|--------|-------------|
| `color-contrast` | serious | Text contrast ≥ 4.5:1 (AA) |
| `link-in-text-block` | serious | Links distinguishable from text |

### Form Rules

| Rule ID | Impact | Description |
|---------|--------|-------------|
| `form-field-multiple-labels` | moderate | Form fields must not have multiple labels |
| `label` | critical | Form inputs must have labels |
| `label-content-name-mismatch` | serious | Visible label matches accessible name |
| `autocomplete-valid` | serious | `autocomplete` attribute must be valid |

### Keyboard Rules

| Rule ID | Impact | Description |
|---------|--------|-------------|
| `accesskeys` | serious | `accesskey` values must be unique |
| `focus-order-semantics` | minor | Focus order should follow semantics |
| `keyboard-hidden` | serious | Focusable elements must not be hidden |
| `keyboard-trap` | serious | Focus must not be trapped |
| `tabindex` | serious | `tabindex` must not exceed 0 |
| `target-size` | serious | Touch targets ≥ 24x24 CSS pixels |

### Images Rules

| Rule ID | Impact | Description |
|---------|--------|-------------|
| `area-alt` | critical | `<area>` elements must have alt text |
| `image-alt` | critical | Images must have alternate text |
| `input-image-alt` | critical | Image inputs must have alt text |
| `svg-img-alt` | serious | SVG images must have accessible name |

### Links Rules

| Rule ID | Impact | Description |
|---------|--------|-------------|
| `link-name` | serious | Links must have discernible text |
| `link-in-text-block` | serious | Links must be distinguishable |
| `identical-links-same-purpose` | minor | Same-purpose links have same name |

### Structure Rules

| Rule ID | Impact | Description |
|---------|--------|-------------|
| `bypass` | serious | Page must have bypass blocks |
| `document-title` | serious | Page must have descriptive title |
| `empty-heading` | minor | Headings must not be empty |
| `heading-order` | moderate | Heading levels must increase sequentially |
| `landmark-one-main` | moderate | Page must have one `main` landmark |
| `page-has-heading-one` | moderate | Page must have an `h1` |

### Language Rules

| Rule ID | Impact | Description |
|---------|--------|-------------|
| `html-has-lang` | serious | `<html>` must have `lang` attribute |
| `html-lang-valid` | serious | `lang` attribute must be valid |
| `valid-lang` | moderate | Lang attributes must be valid |

### Name Role Value Rules

| Rule ID | Impact | Description |
|---------|--------|-------------|
| `button-name` | critical | Buttons must have discernible text |
| `frame-title` | serious | Frames must have title |

### Table Rules

| Rule ID | Impact | Description |
|---------|--------|-------------|
| `td-headers` | serious | Table cells must use headers correctly |
| `th-has-data-cells` | moderate | Header cells must have data cells |
| `table-fake-caption` | serious | Tables must not use first cell as caption |

## Impact Levels

| Impact | Description | Action |
|--------|-------------|--------|
| `critical` | Prevents assistive tech usage | Fix immediately |
| `serious` | Significant barrier to accessibility | Fix soon |
| `moderate` | Partial barrier | Fix in next sprint |
| `minor` | Minor inconvenience | Fix when possible |

## Running Rules by Category

```bash
# ARIA rules only
wavexis axe https://example.com --tags cat.aria

# Color and forms
wavexis axe https://example.com --tags cat.color,cat.forms

# WCAG 2.2 AA
wavexis axe https://example.com --tags wcag2a,wcag2aa,wcag21a,wcag21aa,wcag22a,wcag22aa

# Best practices
wavexis axe https://example.com --tags best-practice

# Specific rules
wavexis axe https://example.com --rules color-contrast,label,image-alt,heading-order

# Exclude rules
wavexis axe https://example.com --tags wcag2aa --exclude-rules region
```

## References

- [axe-core Rule Descriptions](https://github.com/dequelabs/axe-core/blob/develop/doc/rule-descriptions.md)
- [axe-core Tags](https://github.com/dequelabs/axe-core/blob/develop/doc/rule-descriptions.md#tags)
- [Deque University](https://dequeuniversity.com/rules/axe)
