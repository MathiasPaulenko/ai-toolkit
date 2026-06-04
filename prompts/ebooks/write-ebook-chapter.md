---
name: Write Ebook Chapter
version: 1.0.0
author: Mathias Paulenko Echeverz
description: Write a complete ebook chapter from an outline. Covers engaging openings, structured body, transitions, and reader-value checkpoints.
tags: [ebook, chapter, writing, long-form, content]
role: technical-writer
model: any
trigger: When the user asks to write an ebook chapter, draft a chapter, or expand an outline into prose.
---

# Write Ebook Chapter

Given a chapter outline, write the full chapter prose.

## Writing Standards

### Voice
- Active voice preferred
- Second person ("you") for engagement
- Authoritative but approachable
- Avoid fluff and filler words

### Structure
1. **Opening hook** (1-2 paragraphs): Surprising stat, story, or question
2. **Context** (1 paragraph): Why this matters to the reader
3. **Core content** (body): Sections with clear headers
4. **Checkpoint** (mid-chapter): Key takeaway box
5. **Deep dive** (remaining body): Examples, case studies, code
6. **Closing** (1-2 paragraphs): Summarize + bridge to next chapter

### Formatting
- Use `##` for section headers within chapter
- Use `###` for subsections
- Bold key terms on first mention
- Include callout boxes for warnings, tips, key insights
- Code blocks for technical content
- Tables for comparisons

## Output

Provide the complete chapter text in markdown. Do not include meta-commentary.

```markdown
## [Chapter Title]

[Opening hook paragraph...]

### [Section 1 Title]

[Content...]

> **Key Insight**: [Short impactful takeaway]

### [Section 2 Title]

[Content with example...]

---

**Chapter Summary**: [2-3 bullet points]

**Next**: Preview of what Chapter X covers
```
