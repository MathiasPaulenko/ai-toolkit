---
name: Generate Ebook Outline
version: 1.0.0
author: Mathias Paulenko Echeverz
description: Generate a comprehensive ebook outline with chapter structure, subtopics, word count targets, and reader progression logic.
tags: [ebook, outline, structure, content-planning, writing]
role: content-strategist
model: any
trigger: When the user asks to create an ebook outline, structure an ebook, or plan ebook chapters.
---

# Generate Ebook Outline

Given a topic, target audience, and ebook goal, generate a detailed outline.

## Inputs

- **Topic**: Main subject of the ebook
- **Audience**: Skill level, role, industry
- **Goal**: Educate, persuade, entertain, reference
- **Length**: Target word count or page count
- **Format**: PDF, EPUB, interactive, lead magnet

## Output Format

```markdown
# Ebook Outline: [Title]

## Metadata
- **Target audience**: [Description]
- **Total word count**: [X words]
- **Estimated reading time**: [X hours]
- **Difficulty**: Beginner / Intermediate / Advanced

## Chapter Structure

### Chapter 1: [Title] ([word count])
**Hook**: Why this matters now
**Learning objective**: What reader will know
**Sections**:
1. [Subsection] (~300 words)
2. [Subsection] (~500 words)
3. [Subsection] (~400 words)

**Transition**: Bridge to Chapter 2

### Chapter 2: [Title] ([word count])
...

## Content Flow Analysis
- [ ] Problem → Agitation → Solution arc maintained
- [ ] Complexity increases progressively
- [ ] Each chapter builds on previous
- [ ] Actionable takeaways per chapter

## Appendix Plan
- Glossary
- Resources / further reading
- About the author
