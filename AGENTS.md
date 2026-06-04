# AI Agents in ai-toolkit

This repository stores reusable AI agent definitions. Every agent follows a standardized structure and metadata format to ensure consistency and discoverability across tools (Cursor, Claude Dev, Continue, Aider, etc).

This file also serves as the **global repository rules** document that the AI must follow when creating, modifying, or reviewing any resource in this repository.

---

## Repository Conventions (Global Rules)

These conventions apply to **all resource types** (skills, agents, prompts, rules, workflows, tools).

### Naming

| Element | Format | Example |
|---------|--------|---------|
| Folders | `kebab-case` | `my-cool-skill/`, `code-reviewer/` |
| Files | `kebab-case.md` | `api-reference.md`, `python-coding-rules.md` |
| Tags | `kebab-case` | `code-review`, `rest-api` |

### Frontmatter (Mandatory)

All resources MUST include YAML frontmatter:

```yaml
---
name: Display Name
version: 1.0.0
author: Mathias Paulenko Echeverz
description: One-line value proposition
tags: [tag1, tag2, tag3]
---
```

Rules:
- `author` is ALWAYS `Mathias Paulenko Echeverz`.
- `version` follows SemVer (`1.0.0`).
- `tags` are 3-5 specific tags, not generic (`ai`, `code`).

### File Organization

| Folder | Purpose |
|--------|---------|
| `references/` | Markdown docs that extend the main resource (API refs, detailed guides) |
| `assets/` | Executable files the user copies or runs (scripts, templates, configs, images) |

Rules:
- Keep main files concise (~400-500 lines).
- Externalize extended content to `references/`.
- Place runnable scripts and templates in `assets/`.

### Versioning

- Follow [SemVer](https://semver.org/).
- Bump `version` in frontmatter on every significant change.

---

## Directory Structure

```
ai-toolkit/
  agents/
    _template/
      agent.md              # Reference template
    agent-name/             # kebab-case folder
      agent.md              # Agent definition
      knowledge/            # Optional: domain docs, schemas, references
        ref.md
      tools/                # Optional: scripts the agent can invoke
        tool.py
```

## Agent Definition (`agent.md`)

Every agent MUST be a Markdown file with YAML frontmatter followed by structured sections.

### Frontmatter (required)

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

| Field | Description |
|-------|-------------|
| `name` | Human-readable name (Title Case) |
| `version` | SemVer (`1.0.0`) |
| `author` | `Mathias Paulenko Echeverz` |
| `description` | Single-line value proposition |
| `tags` | 3-5 specific tags, not generic (`ai`, `code`) |
| `role` | Identifier used by IDEs to load the agent |
| `type` | Category for grouping agents |
| `language` | Primary language of responses |

### Required Sections

```markdown
# Agent Name

## Role
What persona this agent adopts and its area of expertise.

## Objective
What the agent is meant to achieve in concrete terms.

## Capabilities
- Specific tasks the agent can perform
- Tools or APIs it can invoke
- Knowledge bases it references

## Constraints
- Hard rules the agent must NOT violate
- Boundaries and out-of-scope items

## Knowledge Base
Links to files in `knowledge/` or related skills/rules/tools.

## Communication Style
- Tone (direct, formal, casual)
- Response format (checklists, prose, structured)
- Language preference

## Workflow
Numbered steps the agent follows for its core task.

## Fallback Behavior
What the agent does when uncertain or out of scope.

## References
Links to related resources in this repository.
```

## Naming Conventions

| Element | Format | Example |
|---------|--------|---------|
| Agent folder | `kebab-case` | `repo-guardian/` |
| Agent file | `agent.md` | `agent.md` |
| Knowledge files | `kebab-case.md` | `api-guidelines.md` |
| Tool scripts | `kebab-case.ext` | `validate.py` |
| Tags | `kebab-case` | `code-review`, `security-audit` |

## Agent Types

| Type | Purpose | Examples |
|------|---------|----------|
| `governance` | Enforce standards, review quality | repo-guardian |
| `coding` | Write, refactor, debug code | python-refactorer |
| `review` | PR review, code audit | security-reviewer |
| `creative` | Generate content, designs | ui-designer |
| `research` | Investigate, analyze, summarize | tech-researcher |
| `automation` | CI/CD, deployment, DevOps | deploy-automator |

## Workflow for Creating an Agent

1. **Copy the template** from `agents/_template/agent.md`.
2. **Name the folder** in `kebab-case` matching the agent's purpose.
3. **Fill the frontmatter** with real metadata; no placeholders.
4. **Write all required sections** — incomplete agents are rejected.
5. **Add `knowledge/`** only if the agent needs domain-specific docs.
6. **Add `tools/`** only if the agent invokes scripts.
7. **Self-review** against the checklist below.
8. **Update this file (`AGENTS.md`)** if introducing a new `type`.

## Quality Checklist

### Metadata
- [ ] Frontmatter YAML is present and valid.
- [ ] `name` is descriptive and matches the folder.
- [ ] `version` follows SemVer.
- [ ] `author` is `Mathias Paulenko Echeverz`.
- [ ] `description` explains value in one line.
- [ ] `tags` are specific (3-5 items).
- [ ] `role` and `type` are set.

### Content
- [ ] All 8 required sections are present (Role, Objective, Capabilities, Constraints, Knowledge Base, Communication Style, Workflow, Fallback Behavior).
- [ ] No placeholder text (`Agent Name`, `tu-usuario`, `TODO`, etc.).
- [ ] Constraints are actual prohibitions, not suggestions.
- [ ] Workflow is numbered and actionable.
- [ ] References point to existing files in the repo.

### Structure
- [ ] Folder name is `kebab-case`.
- [ ] `agent.md` is the only required file at root of the agent folder.
- [ ] `knowledge/` and `tools/` are optional but follow naming conventions if present.

## Integration with IDEs

### Cursor
Copy the agent folder to `.cursor/agents/` or reference `agent.md` in Cursor Rules.

### Claude Dev / Claude Code
Reference the `agent.md` path when starting a session or add to `.claude/agents/`.

### Continue
Add the agent to `.continue/config.yaml` under `agents:` pointing to the `agent.md` file.

### Aider
Use the agent content as a system prompt or place in `.aider/agents/`.

## References

- `agents/_template/agent.md` — Template
- `agents/repo-guardian/agent.md` — Benchmark example
- `AGENTS.md` — Global repository conventions and agent standards
