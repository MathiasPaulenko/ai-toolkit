# Security Policy

## Supported Versions

The following versions of ai-toolkit are currently supported with security updates:

| Version | Supported |
|---------|-----------|
| latest `main` | ✅ |
| tagged releases | ✅ |
| older forks | ❌ |

Since this is a documentation and resource repository (no runtime code), security concerns are primarily related to:

- Malicious content in contributed skills, agents, or prompts
- Exposed secrets or credentials in examples or templates
- Insecure patterns in code snippets that could mislead users

## Reporting a Vulnerability

If you discover a security vulnerability or inappropriate content in this repository, please report it responsibly.

**Do NOT open a public issue for security-related problems.**

Instead, email the maintainer at **mathias@mathiaspaulenko.com** with:

1. A description of the vulnerability or concern
2. The affected file(s) and line numbers
3. Steps to reproduce (if applicable)
4. Suggested fix (if any)

You will receive a response within **48 hours** acknowledging receipt. A fix or mitigation will be prioritized based on severity.

## Responsible Disclosure

We ask that you:

- Give us reasonable time to address the issue before any public disclosure
- Avoid accessing or modifying data that does not belong to you
- Act in good faith to protect user privacy and system integrity

## Security Considerations for Contributors

When contributing to this repository:

- **Never** hardcode API keys, tokens, passwords, or other secrets in examples or templates
- Use environment variables or placeholder values (e.g., `<YOUR_API_KEY>`) in code snippets
- Review all code examples for injection vulnerabilities (SQL, command, XSS)
- Ensure that scripts in `assets/` do not execute destructive operations without explicit user consent
- Follow the [OWASP Top 10](https://owasp.org/www-project-top-ten/) guidelines when writing security-related content

## Safe Usage of Resources

When using resources from this repository:

- Review all code snippets before executing them
- Never run scripts from `assets/` without understanding what they do
- Sanitize any user input when adapting templates for production use
- Keep dependencies updated to their latest secure versions

## Contact

For any security-related questions or concerns, contact: **mathias@mathiaspaulenko.com**
