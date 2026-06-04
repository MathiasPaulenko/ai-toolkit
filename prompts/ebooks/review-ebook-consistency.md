---
name: Review Ebook Consistency
version: 1.0.0
author: Mathias Paulenko Echeverz
description: Review an ebook manuscript for internal consistency: terminology, tone, formatting, character names, timeline, and factual accuracy.
tags: [ebook, consistency, review, quality, manuscript]
role: editor
model: any
trigger: When the user asks to review an ebook for consistency, proofread, or quality-check a manuscript.
---

# Review Ebook Consistency

Review a complete ebook manuscript for internal consistency.

## Terminology Audit

- [ ] Key terms defined on first use and used consistently
- [ ] No contradictory definitions
- [ ] Acronyms expanded on first use
- [ ] Product/tool names spelled consistently (e.g., "GitHub" not "Github")

## Tone & Voice

- [ ] Consistent person (second person maintained)
- [ ] Consistent level of formality
- [ ] No sudden shifts to academic or casual tone
- [ ] Authorial voice recognizable throughout

## Formatting

- [ ] Header levels consistent
- [ ] Code block languages specified
- [ ] Callout box styles uniform
- [ ] Figure/table numbering sequential
- [ ] Page references accurate

## Technical Accuracy (if applicable)

- [ ] Code examples are runnable
- [ ] Version numbers consistent with current reality
- [ ] URLs are valid (or clearly marked as examples)
- [ ] Commands work on stated OS/environment

## Narrative Consistency (if applicable)

- [ ] Character names don't change spelling
- [ ] Timeline events are chronological
- [ ] Setting details remain consistent
- [ ] Plot threads resolved

## Output

```markdown
## Consistency Report

### Critical Issues (Fix Before Release)
| Issue | Location | Severity |
|-------|----------|----------|
| [Description] | Ch X, Para Y | High |

### Warnings (Fix If Time)
| Issue | Location | Suggestion |
|-------|----------|------------|
| [Description] | Ch X | [Fix] |

### Pass Count
- Terminology: [X/Y]
- Tone: [X/Y]
- Formatting: [X/Y]
- Technical: [X/Y]

### Overall Verdict
[Pass with minor edits / Needs revision / Release-ready]
```
