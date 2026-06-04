---
name: Create New Agent
version: 1.0.0
author: Mathias Paulenko Echeverz
description: Step-by-step workflow to bootstrap a new agent from the template. Covers copying, filling metadata, writing all required sections, and validation against AGENTS.md standards.
tags: [workflow, agent, scaffolding, template, quality-check]
role: repo-maintainer
---

# Create New Agent

## Prerequisites

- Read `agents/_template/agent.md`.
- Read `AGENTS.md` (standards document).
- Verify the agent name in `kebab-case` is not already taken.

---

## Steps

### 1. Create Directory Structure

```bash
mkdir agents/<agent-name>
mkdir agents/<agent-name>/knowledge  # Optional: domain docs, schemas
mkdir agents/<agent-name>/tools      # Optional: scripts the agent invokes
```

### 2. Copy Template

```bash
cp agents/_template/agent.md agents/<agent-name>/agent.md
```

### 3. Fill Frontmatter

Edit the YAML frontmatter at the top of `agent.md`:

```yaml
---
name: Agent Display Name
version: 1.0.0
author: Mathias Paulenko Echeverz
description: One-line description of what this agent does
tags: [tag1, tag2, tag3]
role: primary-role-identifier
type: governance | coding | review | creative | research | automation
language: en | es
---
```

Rules:
- `name`: Title Case, matches folder name.
- `version`: SemVer (`1.0.0`).
- `author`: Always `Mathias Paulenko Echeverz`.
- `tags`: 3-5 specific kebab-case tags.
- `type`: One of the valid agent types.
- `role`: IDE-compatible identifier.

### 4. Write All Required Sections

Every agent **must** have these 8 sections:

1. **Role** — Persona and area of expertise.
2. **Objective** — Concrete achievement goal.
3. **Capabilities** — Tasks, tools, APIs, knowledge bases.
4. **Constraints** — Hard rules (prohibitions, not suggestions).
5. **Knowledge Base** — Links to `knowledge/` files or related skills.
6. **Communication Style** — Tone, response format, language preference.
7. **Workflow** — Numbered steps for core task.
8. **Fallback Behavior** — What to do when uncertain or out of scope.

### 5. Write Constraints as Prohibitions

Constraints must be actionable rejections:

```markdown
## Constraints

- NEVER approve code containing hardcoded secrets.
- NEVER suggest tests without clear assertions.
- NEVER ignore non-functional requirements.
```

Avoid vague constraints:

```markdown
<!-- Bad -->
- Be careful with security.
- Write good tests.
```

### 6. Add Knowledge Files (Optional)

If the agent needs domain-specific references:

```bash
agents/<agent-name>/knowledge/
  api-guidelines.md
  security-checklist.md
```

Reference them in the **Knowledge Base** section:

```markdown
## Knowledge Base

- `knowledge/api-guidelines.md` — REST API design standards
- `knowledge/security-checklist.md` — OWASP Top 10 mappings
```

### 7. Add Tool Scripts (Optional)

If the agent can invoke scripts:

```bash
agents/<agent-name>/tools/
  validate.py
  scan.sh
```

Document them in **Capabilities**:

```markdown
## Capabilities

- Invoke `tools/validate.py` for automated validation.
- Run `tools/scan.sh` for dependency scanning.
```

### 8. Self-Review Checklist

- [ ] Frontmatter YAML is valid.
- [ ] `name` matches the folder in `kebab-case`.
- [ ] All 8 required sections are present.
- [ ] No placeholder text (`Agent Name`, `TODO`, `your-name`).
- [ ] Constraints are actual prohibitions, not suggestions.
- [ ] Workflow is numbered and actionable.
- [ ] References point to existing files in the repo.
- [ ] `type` is one of: governance, coding, review, creative, research, automation.

### 9. Update TODO.md

Mark the agent as completed in `ref/TODO.md` or move to `ref/COMPLETED.md`.

### 10. Commit

```bash
git add agents/<agent-name>/
git commit -m "feat(agents): add <agent-name> agent"
```
