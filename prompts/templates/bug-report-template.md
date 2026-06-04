---
name: Bug Report Template
version: 1.0.0
author: Mathias Paulenko Echeverz
description: Bug report template with environment details, reproduction steps, expected vs actual behavior, and severity classification.
tags: [bug-report, template, qa, testing, issue]
role: qa-engineer
model: any
trigger: When the user asks for a bug report template or issue reporting format.
---

# Bug Report Template

## Summary

One-line description of the bug.

## Severity

- [ ] Critical — Data loss, security breach, system crash
- [ ] High — Major feature broken, workaround difficult
- [ ] Medium — Feature impaired, workaround exists
- [ ] Low — Cosmetic, minor inconvenience
- [ ] Trivial — Typo, alignment, color

## Environment

| Item | Details |
|------|---------|
| Application Version | v1.2.3 |
| Browser / OS | Chrome 120 / Windows 11 |
| API Version | v2.1 |
| Database | PostgreSQL 16 |
| Deployment | Staging |
| Date / Time | 2024-06-04 14:30 UTC |

## Steps to Reproduce

1. Navigate to `https://app.example.com/login`
2. Enter valid username: `testuser`
3. Enter valid password: `TestPass123`
4. Click "Login" button
5. Observe the error

## Expected Result

User is redirected to the dashboard and session is established.

## Actual Result

Error page 500 is displayed with message "Internal Server Error".

## Evidence

### Screenshot
<!-- Attach screenshot of the error state -->

### Logs
```
2024-06-04 14:30:15 ERROR app.auth: Authentication failed for user 'testuser'
Traceback (most recent call last):
  File "/app/auth.py", line 42, in login
    user = User.query.filter_by(username=username).first()
 sqlalchemy.exc.OperationalError: (psycopg2.OperationalError) connection failed
```

### API Response (if applicable)
```json
{
  "status": 500,
  "error": "Internal Server Error",
  "message": "Database connection failed"
}
```

### Network Tab
<!-- Attach HAR file or relevant request/response -->

## Additional Context

- Does not occur on production
- Occurs consistently on staging
- Started after deployment v1.2.3
- Related to database migration `add_user_indexes`

## Workaround

<!-- If any temporary workaround exists -->

Refresh the page and retry login; succeeds on second attempt.

## Regression

<!-- Mark if this is a regression from a previous version -->

- [ ] This is a regression (worked in previous version)
- Previous working version: v1.2.2

## Root Cause Analysis (if known)

<!-- For QA engineers or developers filling this after investigation -->

Database connection pool exhausted due to missing `pool_recycle` configuration.

## Attachments

- [ ] Screenshot
- [ ] Video recording
- [ ] HAR file
- [ ] Log file
- [ ] Database dump
- [ ] Other: ___________
