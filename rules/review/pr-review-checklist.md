---
name: PR Review Checklist
version: 1.0.0
author: Mathias Paulenko Echeverz
description: Comprehensive checklist for pull request reviews covering security, performance, testing, documentation, and backward compatibility.
tags: [code-review, checklist, pull-request, quality, security]
role: review-checklist
type: rules
language: en
---

# PR Review Checklist

Use this checklist for every pull request review. Mark items as checked only when verified.

## Security

- [ ] No hardcoded secrets, API keys, or credentials in code
- [ ] No SQL injection via string concatenation (parameterized queries used)
- [ ] No XSS vulnerabilities (output escaping or sanitization applied)
- [ ] No path traversal risks in file handling
- [ ] No unsafe deserialization (`pickle.loads`, `ObjectInputStream` without validation)
- [ ] Authentication and authorization checks are server-side
- [ ] Input validation at all entry points
- [ ] CORS configured with explicit allowlists (not `*` in production)
- [ ] Dependencies scanned for known CVEs
- [ ] No disabled certificate validation (`verify=False`, `InsecureSkipVerify`)

## Performance

- [ ] No N+1 queries in database operations
- [ ] Expensive operations are cached where appropriate
- [ ] No unnecessary API calls or data fetches
- [ ] Large payloads are paginated or streamed
- [ ] Images/assets are optimized (compression, correct format)
- [ ] No memory leaks (resource cleanup, connection pooling)
- [ ] Async/await used for I/O-bound operations

## Testing

- [ ] Tests exist for the modified code
- [ ] Tests cover happy path, edge cases, and error paths
- [ ] Assertions are specific and meaningful (not just `assertTrue`)
- [ ] Mocking used for external dependencies
- [ ] No test logic duplication (fixtures/helpers used)
- [ ] Test data factories used instead of hardcoded values
- [ ] Flaky tests identified and stabilized
- [ ] Coverage report attached or threshold met

## Documentation

- [ ] README updated if behavior changes
- [ ] API documentation updated for endpoint changes
- [ ] Code comments explain "why", not "what"
- [ ] Complex logic has inline comments
- [ ] ADR written for architectural decisions
- [ ] Changelog updated for user-facing changes
- [ ] Breaking changes documented with migration steps

## Backward Compatibility

- [ ] No breaking changes to public APIs without deprecation notice
- [ ] Database migrations are reversible (down scripts)
- [ ] Feature flags used for risky changes
- [ ] Client compatibility verified (mobile apps, third-party consumers)
- [ ] Rollback plan documented for deployment changes

## Code Quality

- [ ] Follows project coding standards (see `rules/coding/`)
- [ ] No dead code (unused imports, variables, methods)
- [ ] No commented-out code or debug prints
- [ ] Functions do one thing (< 50 lines, ideally < 30)
- [ ] Meaningful variable and function names
- [ ] Magic numbers extracted to named constants
- [ ] Error handling is explicit (no silent catches)

## Architecture

- [ ] SOLID principles followed (no god classes, tight coupling)
- [ ] Design patterns applied correctly (Repository, Factory, Strategy)
- [ ] Dependencies injected via constructor (not field injection)
- [ ] Business logic in domain layer, not controllers
- [ ] No circular dependencies

## Reviewer Notes

### Approval Levels

| Level | Meaning |
|-------|---------|
| **Approve** | Ready to merge |
| **Comment** | Feedback provided, author decides |
| **Request Changes** | Must fix before merge |

### Required Approvals

- [ ] 1 approval for bug fixes and refactors
- [ ] 2 approvals for feature additions
- [ ] Security team approval for auth/security changes
- [ ] Architecture review for infrastructure changes
