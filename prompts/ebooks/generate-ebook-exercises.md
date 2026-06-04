---
name: Generate Ebook Exercises
version: 1.0.0
author: Mathias Paulenko Echeverz
description: Generate practical exercises, quizzes, and action items for ebook chapters to reinforce learning.
tags: [ebook, exercises, learning, reinforcement, interactive]
role: instructional-designer
model: any
trigger: When the user asks for ebook exercises, practice problems, quizzes, or action items.
---

# Generate Ebook Exercises

Given a chapter's content, generate exercises that reinforce key concepts.

## Exercise Types

### 1. Reflection Questions
- "What was the most surprising insight from this chapter?"
- "How does [concept] apply to your current work?"

### 2. Application Tasks
- "Implement [pattern] in your own codebase"
- "Audit your current setup against the checklist"

### 3. Knowledge Checks (Quiz)
- Multiple choice (3-5 per chapter)
- True/false with explanation
- Fill-in-the-blank for key terms

### 4. Mini-Projects
- Hands-on tasks with expected output
- Progressive difficulty
- Self-assessment rubric

### 5. Discussion Prompts
- For book clubs or study groups
- For team training sessions

## Output Format

```markdown
## Chapter X Exercises

### Reflection (3)
1. [Question]

### Knowledge Check (5)
1. What is the primary purpose of [concept]?
   a) ... b) ... c) ... d) ...
   **Answer**: [Letter] — [Explanation]

### Application Task
**Task**: [Description]
**Expected output**: [What success looks like]
**Time estimate**: [Duration]

### Mini-Project
**Objective**: [What to build/do]
**Requirements**: [Specific criteria]
**Stretch goal**: [Optional advanced version]
```
