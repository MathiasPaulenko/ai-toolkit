---
name: Ebook Writer
version: 1.0.0
author: Mathias Paulenko Echeverz
description: Comprehensive ebook creation skill covering outlining, chapter writing, editing, formatting, and marketing. Supports technical, educational, and narrative ebooks.
tags: [ebook, writing, publishing, content, long-form]
role: content-strategist
model: any
trigger: When the user asks to write, create, or publish an ebook, or needs help with book-length content.
---

# Ebook Writer

End-to-end skill for creating professional ebooks with AI assistance.

## 1. Ebook Types

| Type | Characteristics | Example |
|------|-----------------|---------|
| **Educational** | Step-by-step, exercises, quizzes | "Learn Python in 30 Days" |
| **Technical Reference** | Comprehensive, searchable, examples | "The Kubernetes Handbook" |
| **Thought Leadership** | Opinion, framework, methodology | "The DevOps Mindset" |
| **Narrative / Memoir** | Story-driven, personal | "From Code to CEO" |
| **Lead Magnet** | Short, actionable, solves one problem | "The 5-Minute API Design Checklist" |

## 2. The Ebook Creation Pipeline

```
Idea → Research → Outline → Write → Edit → Format → Publish → Market
```

### Phase 1: Ideation (1-2 hours)
- Define topic, audience, goal
- Validate demand (competitor analysis)
- Choose ebook type and length

### Phase 2: Research (2-4 hours)
- Collect sources, data, examples
- Interview subject matter experts
- Document gaps in existing content

### Phase 3: Outline (2-3 hours)
- Chapter structure with word counts
- Section-level detail
- Content flow logic

### Phase 4: Writing (1-2 weeks)
- Draft one chapter at a time
- Follow the writing prompts
- Include examples, code, diagrams

### Phase 5: Editing (3-5 days)
- Structural edit (flow, logic)
- Line edit (clarity, voice)
- Copy edit (grammar, consistency)
- Technical review (accuracy)

### Phase 6: Formatting (1-2 days)
- Apply ebook typography
- Generate TOC, index
- Prepare cover, front matter
- Export to PDF/EPUB

### Phase 7: Publishing (1 day)
- Upload to platform (Gumroad, Amazon, website)
- Set pricing and distribution
- Configure landing page

### Phase 8: Marketing (ongoing)
- Landing page copy
- Email sequence
- Social media posts
- Affiliate / partnership outreach

## 3. Writing Best Practices

### Voice
- Active voice, second person
- Short paragraphs (3-5 sentences)
- One idea per section
- Use analogies for complex concepts

### Structure per Chapter
1. Hook (story, stat, question)
2. Context (why this matters)
3. Core content (with examples)
4. Checkpoint (key takeaway)
5. Deep dive (advanced content)
6. Closing (summary + bridge)

### Technical Content
- All code must be runnable
- Specify language versions
- Include expected output
- Provide GitHub repo link

## 4. Quality Gates

Before publishing, verify:
- [ ] All chapters complete and edited
- [ ] Consistent terminology throughout
- [ ] Code examples tested
- [ ] Images have alt text
- [ ] Internal links work
- [ ] TOC matches actual content
- [ ] Front matter complete (ISBN if applicable)
- [ ] Marketing copy written
- [ ] Landing page ready

## 5. Tools

- **Writing**: Obsidian, VS Code, Google Docs
- **Formatting**: Pandoc, LaTeX, Vellum
- **Graphics**: Canva, Figma
- **Publishing**: Gumroad, Amazon KDP, Leanpub
- **Marketing**: Mailchimp, ConvertKit

## 6. Related Prompts

Use these prompts from `prompts/ebooks/`:
- `generate-ebook-outline` — Structure and planning
- `research-topic-for-ebook` — Content research
- `generate-ebook-title-options` — Naming
- `write-ebook-introduction` — Opening chapter
- `write-ebook-chapter` — Chapter drafting
- `write-ebook-conclusion` — Closing chapter
- `edit-ebook-chapter` — Revision
- `generate-ebook-case-study` — Real-world examples
- `generate-ebook-exercises` — Learning reinforcement
- `format-ebook-for-export` — PDF/EPUB preparation
- `generate-ebook-marketing-copy` — Promotion
- `review-ebook-consistency` — Quality check
