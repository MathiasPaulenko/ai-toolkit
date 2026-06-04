# ai-toolkit

Personal repository of AI resources: prompts, skills, agents, rules, workflows, and tools created to obtain consistent and structured results with LLMs.

## Resources (135)

| Category | Count |
|-----------|----------|
| [Skills](#skills) | 27 |
| [Agents](#agents) | 10 |
| [Prompts](#prompts) | 64 |
| [Rules](#rules) | 14 |
| [Workflows](#workflows) | 14 |
| [Tools](#tools) | 6 |

### Skills

#### Testing & QA (13)

| Skill | Tags |
|-------|------|
| `behave-bdd` | `python`, `bdd`, `gherkin`, `testing` |
| `allure-reports` | `reporting`, `pytest`, `cypress`, `ci-cd` |
| `robot-framework` | `testing`, `keyword-driven`, `selenium` |
| `jmeter-load-testing` | `jmeter`, `load-testing`, `performance` |
| `sonarqube-quality-gates` | `sonarqube`, `quality-gates`, `static-analysis` |
| `testcontainers` | `integration-testing`, `docker`, `databases`, `kafka` |
| `pytest-advanced` | `pytest`, `python`, `fixtures`, `plugins` |
| `postman-api-automation` | `api-testing`, `postman`, `newman`, `rest` |
| `appium-mobile` | `mobile`, `appium`, `ios`, `android` |
| `karate-api-testing` | `api-testing`, `karate`, `bdd`, `rest` |
| `k6-load-testing` | `load-testing`, `k6`, `performance`, `grafana` |
| `webdriverio` | `e2e`, `webdriverio`, `selenium`, `cross-browser` |
| `xctest-ios` | `ios`, `xctest`, `swift`, `unit-testing` |

#### Development (12)

| Skill | Tags |
|-------|------|
| `flask-api` | `python`, `flask`, `rest`, `api` |
| `android-native` | `kotlin`, `jetpack-compose`, `mvvm`, `mobile` |
| `jinja2-templates` | `python`, `templating`, `flask`, `fastapi` |
| `paramiko-ssh` | `python`, `ssh`, `sftp`, `automation` |
| `wordpress-themes` | `php`, `wordpress`, `cms`, `frontend` |
| `flet-desktop` | `python`, `desktop`, `flutter`, `gui` |
| `sql-server` | `sql-server`, `t-sql`, `mssql`, `azure-sql` |
| `db2-oracle` | `db2`, `oracle`, `plsql`, `enterprise` |
| `salesforce-dev` | `salesforce`, `apex`, `lwc`, `crm` |
| `appian-lowcode` | `appian`, `low-code`, `bpm` |
| `prestashop-module` | `prestashop`, `php`, `e-commerce` |
| `octane-alm` | `octane`, `alm`, `defect-management` |

#### Content & Writing (2)

| Skill | Tags |
|-------|------|
| `ebook-writer` | `ebook`, `writing`, `publishing`, `content` |
| `prompt-engineering-best-practices` | `prompt-engineering`, `llm`, `cot`, `few-shot`, `role-prompting` |

### Agents

#### QA & Testing (7)

| Agent | Type |
|-------|------|
| `test-architect` | `review` |
| `qa-automation-engineer` | `coding` |
| `performance-tester` | `research` |
| `qa-lead` | `governance` |
| `api-tester` | `coding` |
| `accessibility-tester` | `review` |
| `prompt-engineer` | `review` |

#### Development (1)

| Agent | Type |
|-------|------|
| `code-reviewer` | `review` |

#### Security (1)

| Agent | Type |
|-------|------|
| `security-auditor` | `governance` |

#### DevOps (1)

| Agent | Type |
|-------|------|
| `devops-automator` | `automation` |

### Prompts (64)

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
| `generate-bdd-scenario` | BDD / Gherkin |
| `generate-visual-regression-test` | Percy / Chromatic |
| `generate-mutation-test` | Pitest / Stryker |
| `generate-qa-risk-analysis` | Risk matrix |
| `generate-test-data-strategy` | Data masking / GDPR |
| `generate-accessibility-audit` | WCAG / axe |
| `generate-chaos-engineering-tests` | Gremlin / Chaos Mesh |
| `generate-api-fuzzing-scenarios` | Hypothesis / schemathesis |
| `generate-shift-left-strategy` | Shift-left / TDD |
| `generate-test-automation-roi-report` | ROI / Business case |
| `generate-canary-test-strategy` | Canary / Feature flags |

#### Ebook Writing (15)

| Prompt | Focus |
|--------|---------|
| `generate-ebook-outline` | Structure and planning |
| `research-topic-for-ebook` | Content research |
| `generate-ebook-title-options` | Naming and titles |
| `write-ebook-introduction` | Opening chapter |
| `write-ebook-chapter` | Chapter drafting |
| `write-ebook-conclusion` | Closing chapter |
| `edit-ebook-chapter` | Revision and editing |
| `generate-ebook-case-study` | Real-world examples |
| `generate-ebook-exercises` | Learning reinforcement |
| `format-ebook-for-export` | PDF/EPUB preparation |
| `generate-ebook-marketing-copy` | Promotion and sales |
| `review-ebook-consistency` | Quality checking |
| `create-ebook-table-of-contents` | TOC generation |
| `create-ebook-reference-list` | Bibliography |
| `write-ebook-chapter-summary` | Preview copy |

### Rules

#### Coding Standards (4)

| Rule | Category |
|------|-----------|
| `python-coding-rules` | Python |
| `java-coding-rules` | Java |
| `javascript-coding-rules` | JavaScript / TypeScript |
| `sql-coding-rules` | SQL |

#### QA & Testing (7)

| Rule | Category |
|------|-----------|
| `pr-review-checklist` | General review |
| `test-review-rules` | Test quality |
| `test-automation-rules` | E2E automation |
| `performance-testing-rules` | Performance |
| `mobile-testing-rules` | Mobile |
| `api-testing-rules` | API testing |
| `prompt-quality-rules` | Prompt engineering |

#### Behavior (2)

| Rule | Category |
|------|-----------|
| `response-format-rules` | Formatting |
| `response-language-rules` | Language |

#### CI/CD (1)

| Rule | Category |
|------|-----------|
| `ci-cd-testing-rules` | Pipeline testing |

### Workflows

#### DevOps & Deployment (6)

| Workflow | Purpose |
|----------|-----------|
| `deploy-flask-app` | Docker + nginx + CI/CD deployment |
| `deploy-spring-boot-app` | JAR + K8s + health checks |
| `gitlab-ci` | Complete GitLab pipeline |
| `bitbucket-pipelines` | Bitbucket pipeline |
| `kubernetes-deploy` | K8s manifests + Helm |
| `onboard-new-project` | Initial project setup |

#### QA & Testing (5)

| Workflow | Purpose |
|----------|-----------|
| `setup-e2e-automation` | Bootstrap E2E automation with CI/CD |
| `performance-test-session` | Structured performance testing: SLA → script → execute → analyze |
| `visual-regression-setup` | Configure Chromatic/Percy/Loki with baselines and CI |
| `bug-triage` | Structured bug triage process |
| `qa-release-gate` | Quality gate before production release |

#### Content (1)

| Workflow | Purpose |
|----------|-----------|
| `create-ebook` | Ebook creation pipeline |

#### Templates (2)

| Workflow | Purpose |
|----------|-----------|
| `create-new-skill` | Bootstrap a skill from template |
| `create-new-agent` | Bootstrap an agent from template |

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
