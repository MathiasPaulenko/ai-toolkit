# ai-toolkit

Personal repository of AI resources: prompts, skills, agents, rules, workflows, and tools created to obtain consistent and structured results with LLMs.

## Resources (83)

| Category | Count |
|-----------|----------|
| [Skills](#skills) | 17 |
| [Agents](#agents) | 4 |
| [Prompts](#prompts) | 39 |
| [Rules](#rules) | 8 |
| [Workflows](#workflows) | 8 |
| [Tools](#tools) | 6 |

### Skills

| Skill | Tags |
|-------|------|
| `behave-bdd` | `python`, `bdd`, `gherkin`, `testing` |
| `flask-api` | `python`, `flask`, `rest`, `api` |
| `android-native` | `kotlin`, `jetpack-compose`, `mvvm`, `mobile` |
| `jinja2-templates` | `python`, `templating`, `flask`, `fastapi` |
| `allure-reports` | `reporting`, `pytest`, `cypress`, `ci-cd` |
| `robot-framework` | `testing`, `keyword-driven`, `selenium` |
| `paramiko-ssh` | `python`, `ssh`, `sftp`, `automation` |
| `wordpress-themes` | `php`, `wordpress`, `cms`, `frontend` |
| `sonarqube-quality-gates` | `sonarqube`, `quality-gates`, `static-analysis` |
| `flet-desktop` | `python`, `desktop`, `flutter`, `gui` |
| `sql-server` | `sql-server`, `t-sql`, `mssql`, `azure-sql` |
| `db2-oracle` | `db2`, `oracle`, `plsql`, `enterprise` |
| `jmeter-load-testing` | `jmeter`, `load-testing`, `performance` |
| `salesforce-dev` | `salesforce`, `apex`, `lwc`, `crm` |
| `appian-lowcode` | `appian`, `low-code`, `bpm` |
| `prestashop-module` | `prestashop`, `php`, `e-commerce` |
| `octane-alm` | `octane`, `alm`, `defect-management` |

### Agents

| Agent | Type |
|-------|------|
| `code-reviewer` | `review` |
| `test-architect` | `review` |
| `security-auditor` | `governance` |
| `devops-automator` | `automation` |

### Prompts (39)

#### System / Task / Templates (9)

| Prompt | Type |
|--------|------|
| `python-expert` | System |
| `java-spring-expert` | System |
| `qa-engineer` | System |
| `generate-api-tests` | Task |
| `refactor-legacy-code` | Task |
| `write-tech-documentation` | Task |
| `create-docker-compose` | Task |
| `feature-file-template` | Template |
| `pull-request-template` | Template |
| `bug-report-template` | Template |

#### QA Engineering (30)

| Prompt | Focus |
|--------|---------|
| `generate-test-cases-from-requirements` | Test design |
| `generate-api-test-suite` | API testing |
| `generate-e2e-test-scenarios` | E2E / POM |
| `analyze-bug-root-cause` | Bug analysis |
| `generate-performance-test-plan` | Performance |
| `generate-security-test-cases` | Security / OWASP |
| `generate-test-data` | Data generation |
| `generate-accessibility-test-checklist` | a11y / WCAG |
| `generate-mobile-test-strategy` | Mobile / Appium |
| `generate-database-test-scenarios` | DB testing |
| `generate-regression-test-suite` | Regression |
| `generate-ci-cd-quality-gates` | Pipeline gates |
| `generate-test-automation-strategy` | Automation ROI |
| `review-test-code-quality` | Test review |
| `generate-load-test-script` | k6 / Locust |
| `generate-exploratory-test-charter` | Exploratory |
| `validate-user-story-testability` | INVEST / AC review |
| `generate-compatibility-test-matrix` | Cross-browser |
| `generate-test-summary-report` | Reporting |
| `generate-data-migration-test-plan` | Migration |
| `generate-api-contract-test` | Pact / Schema |
| `generate-canary-deployment-health-checks` | Canary deploy |
| `generate-observability-test-plan` | Monitoring |
| `generate-disaster-recovery-test-scenarios` | DR / Backup |
| `generate-qa-interview-questions` | Hiring |
| `generate-test-data-privacy-compliance` | GDPR / HIPAA |
| `generate-test-environment-setup-guide` | Environment |
| `generate-flaky-test-diagnosis` | Flakiness |
| `generate-qa-metrics-dashboard` | KPIs / DORA |

### Rules

| Rule | Category |
|------|-----------|
| `python-coding-rules` | Coding |
| `java-coding-rules` | Coding |
| `javascript-coding-rules` | Coding |
| `sql-coding-rules` | Coding |
| `pr-review-checklist` | Review |
| `test-review-rules` | Review |
| `response-format-rules` | Behavior |
| `response-language-rules` | Behavior |

### Workflows

| Workflow | Purpose |
|----------|-----------|
| `create-new-skill` | Bootstrap a skill from template |
| `create-new-agent` | Bootstrap an agent from template |
| `deploy-flask-app` | Docker + nginx + CI/CD deployment |
| `deploy-spring-boot-app` | JAR + K8s + health checks |
| `gitlab-ci` | Complete GitLab pipeline |
| `bitbucket-pipelines` | Bitbucket pipeline |
| `kubernetes-deploy` | K8s manifests + Helm |
| `onboard-new-project` | Initial project setup |

### Tools

| Tool | Function |
|------|---------|
| `validate-resource` | Validates frontmatter, kebab-case, placeholders |
| `generate-skill-scaffold` | Interactive CLI to create skills |
| `sync-skills-to-cursor` | Copies skills to `.cursor/rules/` |
| `sync-skills-to-claude` | Copies skills to `.claude/agents/` |
| `export-skills-to-md` | Concatenates skills into a single markdown |
| `check-dead-links` | Scans broken URLs in `.md` |

## Structure

| Folder | Content |
|---------|-----------|
| `prompts/` | System, task, and reusable template prompts |
| `skills/` | Structured skills with `SKILL.md` and assets |
| `agents/` | Agent definitions (`agent.md`, knowledge, tools) |
| `rules/` | Code, review, and behavior rules |
| `workflows/` | Step-by-step procedures for repetitive tasks |
| `tools/` | Utilities, scripts, and technical resources |
| `AGENTS.md` | Global repository conventions and agent standards |
| `justfile` | Common commands (`just validate`, `just export`, etc.) |
| `.devin/` | Devin-specific workflows |
| `.cursor/` | Rules and prompts for Cursor |

## Conventions

- Each resource goes in its own folder with a `kebab-case` name
- Skills and agents include a `README.md` or `SKILL.md` / `agent.md`
- YAML frontmatter is used for metadata (author, version, tags, trigger)
- Technical reference material goes in `references/`; executables and templates in `assets/`
- Example templates are in `_template/` within each category

## Quick Start

Copy the desired resource into the model context or reference it from your IDE configuration (Cursor Rules, Devin Workflows, etc.).

## Commands

```bash
# Validate all resources
just validate

# Generate a new skill (interactive)
just generate-skill

# Export skills to markdown
just export

# Check for broken links
just check-links

# Run all validations
just check
```

## License

This project is licensed under [MIT](LICENSE).

For commercial or enterprise use, see the attribution expectations in [NOTICE.md](NOTICE.md).

Copyright (c) 2026 Mathias Paulenko Echeverz
