---
name: Create New Skill
version: 1.0.0
author: Mathias Paulenko Echeverz
description: Step-by-step workflow to bootstrap a new skill from the template. Covers copying, filling metadata, writing core content, externalizing assets, and self-review.
tags: [workflow, skill, scaffolding, template, quality-check]
role: repo-maintainer
---

# Create New Skill

## Prerequisites

- Read `skills/_template/SKILL.md`.
- Read `AGENTS.md` (global repository conventions).
- Verify the skill name in `kebab-case` is not already taken.

---

## Steps

### 1. Create Directory Structure

```bash
mkdir skills/<skill-name>
mkdir skills/<skill-name>/references  # Optional: extended markdown docs
mkdir skills/<skill-name>/assets      # Optional: scripts, templates, configs
```

### 2. Copy Template

```bash
cp skills/_template/SKILL.md skills/<skill-name>/SKILL.md
```

### 3. Fill Frontmatter

Edit the YAML frontmatter at the top of `SKILL.md`:

```yaml
---
name: Skill Display Name
version: 1.0.0
author: Mathias Paulenko Echeverz
description: One-line value proposition
tags: [tag1, tag2, tag3]
role: primary-role-identifier
model: any
trigger: When the user mentions X, Y, or Z.
---
```

Rules:
- `name`: Title Case, descriptive.
- `version`: SemVer (`1.0.0`).
- `author`: Always `Mathias Paulenko Echeverz`.
- `tags`: 3-5 specific kebab-case tags.
- `trigger`: Natural language condition for activation.

### 4. Write Core Content (~400-500 lines)

Structure:

1. **Overview** — What this skill covers and why it matters.
2. **Setup / Installation** — Prerequisites, package install, env setup.
3. **Core Concepts** — 3-5 sections with code examples.
4. **Common Patterns** — Real-world usage patterns.
5. **Best Practices** — Do's and don'ts.
6. **References** — Links to `references/` or external docs.

Guidelines:
- Keep code examples runnable and complete.
- Use fenced code blocks with language tags.
- Prefer tables for comparisons.
- Avoid walls of text; use lists and short paragraphs.

### 5. Externalize Extended Content (Optional)

If a section exceeds ~100 lines or is reference-heavy:

```bash
# Move to references/
echo "## Extended API Reference" > skills/<skill-name>/references/api-reference.md
```

In `SKILL.md`, replace the section with:

```markdown
## Extended API Reference

See `references/api-reference.md` for detailed method signatures and parameters.
```

### 6. Add Assets (Optional)

Place executable scripts, templates, or config files in `assets/`:

```bash
skills/<skill-name>/assets/
  project-template/
    config.ini
    example.py
```

### 7. Self-Review Checklist

- [ ] Frontmatter YAML is valid (no tabs, no trailing spaces).
- [ ] `name` matches the folder name.
- [ ] All required sections are present.
- [ ] No placeholder text (`TODO`, `Agent Name`, etc.).
- [ ] Code examples are syntactically valid.
- [ ] File paths use absolute references in citations.
- [ ] Assets are in `assets/`, references in `references/`.
- [ ] SKILL.md is ≤ 600 lines (externalize if longer).

### 8. Update TODO.md

Mark the skill as completed in `ref/TODO.md` or move to `ref/COMPLETED.md`.

### 9. Commit

```bash
git add skills/<skill-name>/
git commit -m "feat(skills): add <skill-name> skill"
```
