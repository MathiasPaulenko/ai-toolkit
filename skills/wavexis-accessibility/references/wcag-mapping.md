# WCAG 2.2 Criteria to a11y Result Mapping

> Mapping of WCAG 2.2 success criteria to axe-core rules and a11y tree checks.

## WCAG 2.2 Overview

WCAG 2.2 has 86 success criteria organized into 4 principles:

| Principle | Description | Criteria count |
|-----------|-------------|----------------|
| Perceivable | Information must be presentable in ways users can perceive | 25 |
| Operable | Interface components and navigation must be operable | 28 |
| Understandable | Information and operation of UI must be understandable | 21 |
| Robust | Content must be robust enough for assistive technologies | 12 |

### Conformance levels

| Level | Description | axe tag |
|-------|-------------|---------|
| A | Minimum compliance | `wcag2a`, `wcag21a`, `wcag22a` |
| AA | Standard compliance (target for most organizations) | `wcag2aa`, `wcag21aa`, `wcag22aa` |
| AAA | Enhanced compliance (not required for all content) | `wcag2aaa`, `wcag21aaa` |

## Perceivable (1.x)

### 1.1 Text Alternatives

| Criterion | Level | axe Rules | a11y Tree Check |
|-----------|-------|-----------|-----------------|
| 1.1.1 Non-text Content | A | `image-alt`, `area-alt`, `input-image-alt`, `svg-img-alt` | `image` role nodes must have `name` |

### 1.2 Time-based Media

| Criterion | Level | axe Rules | a11y Tree Check |
|-----------|-------|-----------|-----------------|
| 1.2.1 Audio-only and Video-only | A | `audio-caption`, `video-caption` | Manual check |
| 1.2.2 Captions (Prerecorded) | A | `video-caption` | Manual check |
| 1.2.3 Audio Description or Media Alternative | A | `video-description` | Manual check |
| 1.2.4 Captions (Live) | AA | — | Manual check |
| 1.2.5 Audio Description (Prerecorded) | AA | `video-description` | Manual check |

### 1.3 Adaptable

| Criterion | Level | axe Rules | a11y Tree Check |
|-----------|-------|-----------|-----------------|
| 1.3.1 Info and Relationships | A | `heading-order`, `landmark-one-main`, `definition-list`, `list`, `table-duplicate-name` | Check `role` matches semantic HTML |
| 1.3.2 Meaningful Sequence | A | `tabindex`, `focus-order-semantics` | Check `child_ids` order |
| 1.3.3 Sensory Characteristics | A | — | Manual check |
| 1.3.4 Orientation | AA | `meta-viewport` | Check viewport meta |
| 1.3.5 Identify Input Purpose | AA | `autocomplete-valid` | Check `autocomplete` attribute |
| 1.3.6 Identify Purpose | AAA | — | Manual check |

### 1.4 Distinguishable

| Criterion | Level | axe Rules | a11y Tree Check |
|-----------|-------|-----------|-----------------|
| 1.4.1 Use of Color | A | `link-in-text-block` | Manual check |
| 1.4.2 Audio Control | A | — | Manual check |
| 1.4.3 Contrast (Minimum) | AA | `color-contrast` | Manual check |
| 1.4.4 Resize Text | AA | `meta-viewport` | Check viewport meta |
| 1.4.5 Images of Text | AA | `image-alt` | Manual check |
| 1.4.10 Reflow | AA | — | Manual check |
| 1.4.11 Non-text Contrast | AA | `color-contrast`, `non-text-contrast` | Manual check |
| 1.4.12 Text Spacing | AA | — | Manual check |
| 1.4.13 Content on Hover or Focus | AA | `aria-hidden-focus` | Manual check |

## Operable (2.x)

### 2.1 Keyboard Accessible

| Criterion | Level | axe Rules | a11y Tree Check |
|-----------|-------|-----------|-----------------|
| 2.1.1 Keyboard | A | `keyboard-hidden`, `page-has-heading-one` | Check `focusable` on interactive nodes |
| 2.1.2 No Keyboard Trap | A | `keyboard-trap` | Manual check |
| 2.1.3 Keyboard (No Exception) | AAA | — | Manual check |

### 2.2 Enough Time

| Criterion | Level | axe Rules | a11y Tree Check |
|-----------|-------|-----------|-----------------|
| 2.2.1 Timing Adjustable | A | — | Manual check |
| 2.2.2 Pause, Stop, Hide | A | — | Manual check |

### 2.3 Seizures and Physical Reactions

| Criterion | Level | axe Rules | a11y Tree Check |
|-----------|-------|-----------|-----------------|
| 2.3.1 Three Flashes or Below | A | — | Manual check |
| 2.3.2 Three Flashes | AAA | — | Manual check |
| 2.3.3 Animation from Interactions | AAA | `no-autoplay-audio` | Manual check |

### 2.4 Navigable

| Criterion | Level | axe Rules | a11y Tree Check |
|-----------|-------|-----------|-----------------|
| 2.4.1 Bypass Blocks | A | `bypass`, `landmark-one-main` | Check for `main` or `navigation` roles |
| 2.4.2 Page Titled | A | `document-title` | Check `WebArea` node `name` |
| 2.4.3 Focus Order | A | `tabindex`, `focus-order-semantics` | Check `focusable` order |
| 2.4.4 Link Purpose (In Context) | A | `link-name` | Check `link` nodes have `name` |
| 2.4.5 Multiple Ways | AA | — | Manual check |
| 2.4.6 Headings and Labels | AA | `empty-heading`, `heading-order` | Check `heading` nodes have `name` |
| 2.4.7 Focus Visible | AA | `focus-visible` | Manual check |
| 2.4.8 Location | AAA | `breadcrumb` | Check `navigation` role with breadcrumb name |
| 2.4.9 Link Purpose (Link Only) | AAA | `link-name` | Check `link` nodes have descriptive `name` |
| 2.4.10 Section Headings | AAA | `heading-order` | Check `heading` nodes in sections |
| 2.4.11 Focus Not Obscured (Minimum) | AA | — | Manual check |
| 2.4.12 Focus Not Obscured (Enhanced) | AAA | — | Manual check |
| 2.4.13 Focus Appearance | AAA | — | Manual check |

### 2.5 Input Modalities

| Criterion | Level | axe Rules | a11y Tree Check |
|-----------|-------|-----------|-----------------|
| 2.5.1 Pointer Gestures | A | — | Manual check |
| 2.5.2 Pointer Cancellation | A | — | Manual check |
| 2.5.3 Label in Name | A | `label-content-name-mismatch` | Check `name` includes visible label text |
| 2.5.4 Motion Actuation | A | — | Manual check |
| 2.5.7 Dragging Movements | AA | — | Manual check |
| 2.5.8 Target Size (Minimum) | AA | `target-size` | Check interactive element sizes |

## Understandable (3.x)

### 3.1 Readable

| Criterion | Level | axe Rules | a11y Tree Check |
|-----------|-------|-----------|-----------------|
| 3.1.1 Language of Page | A | `html-has-lang`, `html-lang-valid` | Check `WebArea` `language` property |
| 3.1.2 Language of Parts | AA | `valid-lang` | Check `language` property on nodes |

### 3.2 Predictable

| Criterion | Level | axe Rules | a11y Tree Check |
|-----------|-------|-----------|-----------------|
| 3.2.1 On Focus | A | `no-focus-change` | Manual check |
| 3.2.2 On Input | A | `no-autocomplete` | Manual check |
| 3.2.3 Consistent Navigation | AA | `identical-links-same-purpose` | Manual check |
| 3.2.4 Consistent Identification | AA | `consistent-locale` | Manual check |

### 3.3 Input Assistance

| Criterion | Level | axe Rules | a11y Tree Check |
|-----------|-------|-----------|-----------------|
| 3.3.1 Error Identification | A | `form-field-multiple-labels` | Manual check |
| 3.3.2 Labels or Instructions | A | `label`, `form-field-multiple-labels` | Check `textbox` nodes have `name` |
| 3.3.3 Error Suggestion | AA | `aria-required-attr` | Manual check |
| 3.3.4 Error Prevention (Legal, Financial) | AA | — | Manual check |
| 3.3.7 Redundant Entry | A | — | Manual check |
| 3.3.8 Accessible Authentication (Minimum) | AA | `autocomplete-valid` | Manual check |

## Robust (4.x)

### 4.1 Compatible

| Criterion | Level | axe Rules | a11y Tree Check |
|-----------|-------|-----------|-----------------|
| 4.1.2 Name, Role, Value | A | `button-name`, `link-name`, `aria-valid-attr`, `aria-required-attr`, `aria-valid-attr-value` | Check all interactive nodes have `name` and `role` |
| 4.1.3 Status Messages | AA | `aria-roles`, `aria-valid-attr` | Check for `status` or `alert` roles |

## New in WCAG 2.2

| Criterion | Level | axe Rules | Description |
|-----------|-------|-----------|-------------|
| 2.4.11 Focus Not Obscured (Minimum) | AA | — | Focus must not be hidden |
| 2.4.12 Focus Not Obscured (Enhanced) | AAA | — | Focus must not be partially hidden |
| 2.4.13 Focus Appearance | AAA | — | Focus indicator must be visible |
| 2.5.7 Dragging Movements | AA | — | Alternative to dragging |
| 2.5.8 Target Size (Minimum) | AA | `target-size` | Touch targets ≥ 24x24 CSS pixels |
| 3.2.6 Consistent Help | A | — | Help mechanism in same relative order |
| 3.3.7 Redundant Entry | A | — | Don't ask for same info twice |
| 3.3.8 Accessible Authentication (Minimum) | AA | `autocomplete-valid` | No cognitive function tests |

## Using This Mapping

### With axe command

```bash
# Check WCAG 2.2 Level A and AA
wavexis axe https://example.com \
    --tags wcag2a,wcag2aa,wcag21a,wcag21aa,wcag22a,wcag22aa \
    --output results.json
```

### With a11y_tree

```bash
# Capture tree and check manually
wavexis a11y_tree https://example.com --output tree.json
```

### Mapping results to WCAG

1. Run `wavexis axe` with appropriate `--tags`
2. Read the `violations` array in the results
3. Look up each violation's `id` in the mapping above
4. Identify the WCAG criterion and level
5. Fix the issue and re-run

## References

- [WCAG 2.2](https://www.w3.org/TR/WCAG22/)
- [axe-core Rules](https://github.com/dequelabs/axe-core/blob/develop/doc/rule-descriptions.md)
- [WAI-ARIA Authoring Practices](https://www.w3.org/WAI/ARIA/apg/)
