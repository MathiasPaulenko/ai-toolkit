---
name: Generate Security Test Cases
version: 1.0.0
author: Mathias Paulenko Echeverz
description: Generate security test cases covering OWASP Top 10, injection flaws, authentication weaknesses, and input validation.
tags: [qa, security, owasp, pentest, vulnerability, auth]
role: qa-engineer
model: any
trigger: When the user asks for security tests, OWASP testing, penetration test cases, or vulnerability checks.
---

# Generate Security Test Cases

Generate a comprehensive security test suite based on OWASP Top 10 and application attack surface.

## OWASP Top 10 Coverage

| # | Category | Test Examples |
|---|----------|---------------|
| 1 | Broken Access Control | IDOR, path traversal, forced browsing |
| 2 | Cryptographic Failures | Weak TLS, hardcoded secrets, weak hashing |
| 3 | Injection | SQLi, NoSQLi, LDAP, XPath, Command injection |
| 4 | Insecure Design | Business logic flaws, race conditions |
| 5 | Security Misconfiguration | Default creds, verbose errors, exposed admin |
| 6 | Vulnerable Components | Outdated dependencies, known CVEs |
| 7 | Auth Failures | Brute force, session fixation, JWT flaws |
| 8 | Data Integrity Failures | Unsigned tokens, deserialization |
| 9 | Logging Failures | Missing audit logs, sensitive data in logs |
| 10 | SSRF | Internal service access via user input |

## Test Case Format

```markdown
| ID | Vulnerability | Test Input | Expected Result | Tool |
|----|-------------|------------|-----------------|------|
| SEC-001 | SQL Injection | `admin' OR '1'='1` | Input sanitized, no data leak | sqlmap |
| SEC-002 | XSS (Stored) | `<script>alert(1)</script>` | HTML encoded in output | Burp Suite |
| SEC-003 | IDOR | Change URL param `order_id=123` to `124` | 403 Forbidden (not your order) | Manual |
| SEC-004 | JWT None Alg | Token with `"alg":"none"` | Rejected by server | jwt_tool |
```

## Outputs

- Burp Suite / OWASP ZAP test scripts
- API security tests (authentication bypass)
- Fuzzing payloads for input fields
- Report template with CVSS scoring
