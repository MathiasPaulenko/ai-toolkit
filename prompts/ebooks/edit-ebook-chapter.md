---
name: Edit Ebook Chapter
version: 1.0.0
author: Mathias Paulenko Echeverz
description: Edit an ebook chapter for clarity, flow, consistency, and reader engagement. Fix passive voice, jargon, transitions, and pacing.
tags: [ebook, editing, clarity, flow, revision]
role: editor
model: any
trigger: When the user asks to edit an ebook chapter, review prose, or improve readability.
---

# Edit Ebook Chapter

Given a draft chapter, edit for clarity, flow, and impact.

## Editing Checklist

### Structural
- [ ] Opening hook grabs attention in 2 sentences
- [ ] Each section has a clear purpose
- [ ] Transitions between sections are smooth
- [ ] Closing summarizes and bridges forward
- [ ] Chapter length matches target word count

### Clarity
- [ ] No sentences > 25 words without good reason
- [ ] Jargon explained on first use
- [ ] Analogies used for complex concepts
- [ ] Active voice > 80%
- [ ] One idea per paragraph

### Engagement
- [ ] Second person pronouns present
- [ ] Questions used to provoke thought
- [ ] Examples / anecdotes included
- [ ] Callout boxes for key insights
- [ ] No fluff words (very, really, just, actually)

### Consistency
- [ ] Terminology consistent throughout
- [ ] Tone matches ebook voice
- [ ] Formatting follows style guide
- [ ] Code examples runnable (if technical)

## Output

Provide:
1. **Edited chapter** (full text)
2. **Change log** (significant edits made)
3. **Score** (before/after readability score)

```markdown
## Change Log
| Issue | Location | Fix |
|-------|----------|-----|
| Passive voice | Para 3 | Rewrote as active |
| Missing transition | End of Sec 2 | Added bridge sentence |
```
