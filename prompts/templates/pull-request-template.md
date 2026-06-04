---
name: Pull Request Template
version: 1.0.0
author: Mathias Paulenko Echeverz
description: PR description template with checklist, test evidence, breaking changes, and review readiness criteria.
tags: [pull-request, template, github, gitlab, bitbucket, code-review]
role: developer
model: any
trigger: When the user asks for a pull request template or PR description format.
---

# Pull Request Template

## Title

```
<type>: <short description>
```

Types: `feat`, `fix`, `refactor`, `test`, `docs`, `chore`, `security`

Example: `feat: add JWT authentication to login endpoint`

## Description

### What
Briefly describe what this PR does.

### Why
Explain the motivation and context (link to issue if applicable).

### How
Describe the approach taken and key implementation decisions.

## Changes

- [ ] Feature implementation
- [ ] Bug fix
- [ ] Refactoring
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] Breaking change (see below)

## Testing

### Evidence
<!-- Attach screenshots, logs, or test output -->

- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing performed
- [ ] Edge cases covered

### Test Commands
```bash
# Run the test suite
pytest tests/
# Or specific test
pytest tests/test_auth.py -v
```

## Checklist

- [ ] Code follows project conventions (`AGENTS.md` standards)
- [ ] Self-review completed
- [ ] No hardcoded secrets or credentials
- [ ] Error handling implemented
- [ ] Logging added where appropriate
- [ ] Type hints / generics added (if applicable)
- [ ] No commented-out code or debug prints
- [ ] Documentation updated (README, API docs, ADRs)

## Breaking Changes

<!-- Delete this section if not applicable -->

- **API Change:** `POST /api/v1/login` now returns `access_token` instead of `token`
- **Migration:** Run `flask db migrate` to apply schema changes
- **Config:** New required env var `JWT_SECRET_KEY`

## Related Issues

Closes #123
Relates to #456

## Screenshots (if UI change)

<!-- Attach before/after screenshots -->

## Reviewer Notes

<!-- Specific areas where feedback is needed -->

- Security review needed for auth changes
- Performance impact on login endpoint
