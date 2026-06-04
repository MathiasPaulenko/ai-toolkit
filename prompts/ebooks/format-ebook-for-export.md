---
name: Format Ebook for Export
version: 1.0.0
author: Mathias Paulenko Echeverz
description: Format ebook markdown for export to PDF, EPUB, or print-ready formats. Covers typography, page breaks, TOC generation, and front matter.
tags: [ebook, formatting, export, typography, pandoc]
role: formatter
model: any
trigger: When the user asks to format an ebook, prepare for export, or convert markdown to PDF/EPUB.
---

# Format Ebook for Export

Format ebook markdown for professional export.

## Front Matter

```markdown
---
title: "[Ebook Title]"
author: "[Author Name]"
date: "[Date]"
rights: "© [Year] [Author]. All rights reserved."
language: en
---
```

## Typography Standards

### Headers
- `H1` (#): Part titles only
- `H2` (##): Chapter titles
- `H3` (###): Section titles
- `H4` (####): Subsection titles

### Body
- Font: Georgia or Merriweather for body
- Code: Fira Code or Source Code Pro
- Line height: 1.6 for body, 1.4 for code
- Paragraph indent: 1.5em (print) / none with spacing (digital)

### Page Breaks
```markdown
<div style="page-break-after: always;"></div>
```

## Output Formats

### PDF (pandoc)
```bash
pandoc ebook.md -o ebook.pdf \
  --pdf-engine=xelatex \
  --template=ebook-template.tex \
  --toc --toc-depth=2
```

### EPUB
```bash
pandoc ebook.md -o ebook.epub \
  --epub-cover-image=cover.png \
  --toc --toc-depth=2
```

### HTML
```bash
pandoc ebook.md -o ebook.html \
  --css=style.css \
  --standalone
```

## Quality Checks
- [ ] All images have alt text
- [ ] Internal links work
- [ ] Code blocks are syntax-highlighted
- [ ] Tables fit within page width
- [ ] No widows/orphans in paragraphs
