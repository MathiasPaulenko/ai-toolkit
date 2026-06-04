---
name: Create Ebook Table of Contents
version: 1.0.0
author: Mathias Paulenko Echeverz
description: Generate a professional table of contents for an ebook with page estimates, reading time, and logical flow analysis.
tags: [ebook, toc, table-of-contents, navigation, structure]
role: content-strategist
model: any
trigger: When the user asks for an ebook table of contents, TOC, or navigation structure.
---

# Create Ebook Table of Contents

Generate a professional TOC for an ebook.

## TOC Requirements

### Depth
- Main TOC: Parts, Chapters
- Chapter-level TOC: Sections, Subsections (optional)

### Metadata per Entry
- Chapter title
- Page estimate
- Reading time
- Key topic keywords

### Logic Checks
- [ ] Progressive difficulty (if instructional)
- [ ] Narrative arc (if story-driven)
- [ ] Modular design (if reference)
- [ ] No orphaned prerequisites

## Output Format

```markdown
# Table of Contents

## Part I: [Part Title] ([page range])

**Overview**: [1-2 sentence summary]

| Chapter | Title | Pages | Time | Keywords |
|---------|-------|-------|------|----------|
| 1 | [Title] | 12-15 | 25m | [terms] |
| 2 | [Title] | 18-22 | 35m | [terms] |

---

## Part II: [Part Title] ([page range])

...

## Appendix
- A. [Title] — [page range]
- B. [Title] — [page range]

## Index
[Estimated entries: X]
```
