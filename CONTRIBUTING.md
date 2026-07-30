# Contributing to ai-toolkit

Thank you for your interest in contributing to ai-toolkit! This document outlines the process for contributing to this repository.

## Getting Started

1. Fork the repository on GitHub.
2. Clone your fork locally:

   ```bash
   git clone https://github.com/<your-username>/ai-toolkit.git
   cd ai-toolkit
   ```

3. Create a new branch for your contribution:

   ```bash
   git checkout -b feat/your-feature-name
   ```

## Repository Structure

| Folder | Content |
|---------|-----------|
| `skills/` | Structured skills with `SKILL.md` and assets |
| `agents/` | Agent definitions (`agent.md`, knowledge, tools) |
| `prompts/` | System, task, and reusable template prompts |
| `rules/` | Code, review, and behavior rules |
| `workflows/` | Step-by-step procedures for repetitive tasks |
| `tools/` | Utilities, scripts, and technical resources |

## Conventions

Before contributing, please review the [AGENTS.md](AGENTS.md) file for detailed conventions.

### Naming

- Folders and files use `kebab-case` (e.g., `my-cool-skill/`, `api-reference.md`)
- Tags are `kebab-case` and specific (3-5 items, avoid generic tags like `ai` or `code`)

### Frontmatter

All resources must include YAML frontmatter:

```yaml
---
name: Display Name
version: 1.0.0
author: Mathias Paulenko Echeverz
description: One-line value proposition
tags: [tag1, tag2, tag3]
---
```

- `version` follows [SemVer](https://semver.org/)
- `author` is always `Mathias Paulenko Echeverz`

### File Organization

- Keep main files concise (~400-500 lines)
- Externalize extended content to `references/`
- Place runnable scripts and templates in `assets/`
- Example templates are in `_template/` within each category

## Adding a New Skill

1. Copy the template from `skills/_template/`:

   ```bash
   cp -r skills/_template/ skills/your-skill-name/
   ```

2. Rename the folder to a `kebab-case` name matching your skill's purpose.
3. Fill in the `SKILL.md` with real metadata and content (no placeholders).
4. Add `references/` for extended documentation if needed.
5. Add `assets/` for executable scripts or templates if needed.

## Adding a New Agent

1. Copy the template from `agents/_template/`:

   ```bash
   cp -r agents/_template/ agents/your-agent-name/
   ```

2. Fill in all required sections: Role, Objective, Capabilities, Constraints, Knowledge Base, Communication Style, Workflow, Fallback Behavior, References.
3. Add `knowledge/` for domain-specific docs if needed.
4. Add `tools/` for scripts the agent can invoke if needed.

## Adding a New Workflow

Create a new `kebab-case.md` file in `workflows/` with:

- Clear prerequisites
- Numbered, actionable steps
- Code examples where relevant
- Troubleshooting section
- Checklist for verification

## Validation

Before submitting, validate your resources:

```bash
# Validate all resources
just validate

# Run all checks
just check

# Check for broken links
just check-links
```

### Quality Checklist

- [ ] Frontmatter YAML is present and valid
- [ ] `name` is descriptive and matches the folder
- [ ] `version` follows SemVer
- [ ] `author` is `Mathias Paulenko Echeverz`
- [ ] `tags` are specific (3-5 items)
- [ ] No placeholder text (`TODO`, `tu-usuario`, etc.)
- [ ] Folder name is `kebab-case`
- [ ] All required sections are present
- [ ] References point to existing files in the repo

## Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```text
<type>(<scope>): <description>

<optional body>
```

Common types:

- `feat`: A new feature or resource
- `fix`: A bug fix
- `docs`: Documentation changes
- `refactor`: Code restructuring without behavior change
- `chore`: Maintenance tasks

Examples:

```text
feat(skills): add playwright-e2e skill with visual regression templates
fix(agents): correct frontmatter version in qa-lead agent
docs(readme): update resource count and add new skill section
```

## Pull Requests

1. Ensure your branch is up to date with `main`:

   ```bash
   git fetch origin
   git rebase origin/main
   ```

2. Push your branch:

   ```bash
   git push origin feat/your-feature-name
   ```

3. Open a Pull Request on GitHub using the provided template.
4. Ensure all CI checks pass.
5. Address review feedback if requested.

## Reporting Issues

Use the appropriate issue template when opening a new issue:

- **Bug report**: For unexpected behavior or errors
- **Feature request**: For new skills, agents, rules, or workflows
- **Documentation**: For improvements to existing docs

## Code of Conduct

By participating in this project, you agree to abide by the [Code of Conduct](CODE_OF_CONDUCT.md).

## License

By contributing, you agree that your contributions will be licensed under the [MIT License](LICENSE).

## Questions?

Feel free to open an issue with the `question` label or contact the maintainer at mathias@mathiaspaulenko.com.
