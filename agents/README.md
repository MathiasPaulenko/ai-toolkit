# Agents

Structured AI agent definitions for use across IDEs and tools.
Each agent defines a persona, objective, capabilities, constraints,
and workflow for a specific role.

## Format

Each agent is a folder named in `kebab-case` containing at least
an `agent.md` file with this structure:

```markdown
---
name: Agent Name
version: 1.0.0
author: Mathias Paulenko Echeverz
description: One-line description
tags: [tag1, tag2, tag3]
role: agent-identifier
type: governance | coding | review | creative | research | automation
language: en | es
---

# Agent Name

## Role
What persona this agent adopts.

## Objective
What the agent is meant to achieve.

## Capabilities

- ...

## Constraints

- ...

## Workflow

1. ...

## References

- Links to related resources
```

Optional `knowledge/` and `tools/` folders extend the agent with
domain docs and executable scripts.

## Agents by Category

### DevOps (1)

| Agent | Description | Type |
| --- | --- | --- |
| [`devops-automator`](agents/devops-automator/agent.md) | DevOps agent that generates CI/CD pipelines, Dockerfiles, Kubernetes manifests, Terraform configs, and infrastructure-as-code based on project requirements and best practices. | `automation` |

### Development (1)

| Agent | Description | Type |
| --- | --- | --- |
| [`code-reviewer`](agents/code-reviewer/agent.md) | Pull request reviewer that enforces Clean Code, SOLID principles, design patterns, and language-specific conventions for Python, Java, and JavaScript/TypeScript codebases. | `review` |

### QA & Testing (7)

| Agent | Description | Type |
| --- | --- | --- |
| [`accessibility-tester`](agents/accessibility-tester/agent.md) | Specialist in web and mobile accessibility testing. Audits against WCAG 2.2, tests with screen readers, validates keyboard navigation, and ensures inclusive design. | `review` |
| [`api-tester`](agents/api-tester/agent.md) | Specialist in API testing across REST, GraphQL, gRPC, and SOAP. Designs contract tests, validates schemas, tests error paths, and integrates with CI/CD. | `coding` |
| [`performance-tester`](agents/performance-tester/agent.md) | Designs and executes performance tests, analyzes bottlenecks, and correlates APM metrics with load test results. Covers load, stress, soak, and spike testing. | `research` |
| [`prompt-engineer`](agents/prompt-engineer/agent.md) | Specialist in prompt engineering: reviews, optimizes, and creates prompts using Chain-of-Thought, Few-shot, Role Prompting, and structured output techniques. Ensures prompt quality, consistency, and reliability. | `review` |
| [`qa-automation-engineer`](agents/qa-automation-engineer/agent.md) | Designs, builds, and maintains test automation frameworks. Covers framework selection, Page Object Model, reporting, CI/CD integration, and test stability. | `coding` |
| [`qa-lead`](agents/qa-lead/agent.md) | QA leader for test strategy, team structure, metrics dashboards, hiring interviews, and quality gates. Bridges engineering and business stakeholders on release readiness. | `governance` |
| [`test-architect`](agents/test-architect/agent.md) | Test architect that designs test strategies, creates test plans, selects testing layers (unit, integration, e2e), and generates test matrices for features and user stories. | `coding` |

### Security (1)

| Agent | Description | Type |
| --- | --- | --- |
| [`security-auditor`](agents/security-auditor/agent.md) | Security auditor that scans code and infrastructure for OWASP Top 10 risks, injection flaws, auth weaknesses, insecure dependencies, and misconfigurations. | `review` |

### Wave Ecosystem (3)

| Agent | Description | Type |
| --- | --- | --- |
| [`wave-automation-engineer`](agents/wave-automation-engineer/agent.md) | Browser automation engineer expert in the Wave ecosystem. Writes, debugs, and optimizes automation scripts using cdpwave, bidiwave, wavexis, and wavexis-mcp. | `coding` |
| [`wave-mcp-orchestrator`](agents/wave-mcp-orchestrator/agent.md) | Orchestrator for wavexis-mcp in multi-agent and LLM workflows. Configures and orchestrates MCP sessions across LLM clients (Claude, Cursor, Windsurf, VS Code). | `automation` |
| [`wave-test-architect`](agents/wave-test-architect/agent.md) | Test architect specializing in cross-browser test strategy with the Wave ecosystem. Designs test pyramids, parallel execution, and CI/CD pipelines using cdpwave and bidiwave. | `review` |

## Validation

Run the resource validator to check frontmatter and conventions:

```bash
python tools/validate-resource/validate.py
```
