# ai-toolkit

Personal repository of AI resources: prompts, skills, agents, rules, workflows, and tools created to obtain consistent and structured results with LLMs.

## Resources (136)

| Category | Count |
|-----------|----------|
| [Skills](#skills) | 27 |
| [Agents](#agents) | 10 |
| [Prompts](#prompts) | 65 |
| [Rules](#rules) | 14 |
| [Workflows](#workflows) | 14 |
| [Tools](#tools) | 6 |

### Skills

#### Testing & QA (13)

| Skill | Tags |
|-------|------|
| [`behave-bdd`](skills/behave-bdd/SKILL.md) | `python`, `bdd`, `gherkin`, `testing` |
| [`allure-reports`](skills/allure-reports/SKILL.md) | `reporting`, `pytest`, `cypress`, `ci-cd` |
| [`robot-framework`](skills/robot-framework/SKILL.md) | `testing`, `keyword-driven`, `selenium` |
| [`jmeter-load-testing`](skills/jmeter-load-testing/SKILL.md) | `jmeter`, `load-testing`, `performance` |
| [`sonarqube-quality-gates`](skills/sonarqube-quality-gates/SKILL.md) | `sonarqube`, `quality-gates`, `static-analysis` |
| [`testcontainers`](skills/testcontainers/SKILL.md) | `integration-testing`, `docker`, `databases`, `kafka` |
| [`pytest-advanced`](skills/pytest-advanced/SKILL.md) | `pytest`, `python`, `fixtures`, `plugins` |
| [`postman-api-automation`](skills/postman-api-automation/SKILL.md) | `api-testing`, `postman`, `newman`, `rest` |
| [`appium-mobile`](skills/appium-mobile/SKILL.md) | `mobile`, `appium`, `ios`, `android` |
| [`karate-api-testing`](skills/karate-api-testing/SKILL.md) | `api-testing`, `karate`, `bdd`, `rest` |
| [`k6-load-testing`](skills/k6-load-testing/SKILL.md) | `load-testing`, `k6`, `performance`, `grafana` |
| [`webdriverio`](skills/webdriverio/SKILL.md) | `e2e`, `webdriverio`, `selenium`, `cross-browser` |
| [`xctest-ios`](skills/xctest-ios/SKILL.md) | `ios`, `xctest`, `swift`, `unit-testing` |

#### Development (12)

| Skill | Tags |
|-------|------|
| [`flask-api`](skills/flask-api/SKILL.md) | `python`, `flask`, `rest`, `api` |
| [`android-native`](skills/android-native/SKILL.md) | `kotlin`, `jetpack-compose`, `mvvm`, `mobile` |
| [`jinja2-templates`](skills/jinja2-templates/SKILL.md) | `python`, `templating`, `flask`, `fastapi` |
| [`paramiko-ssh`](skills/paramiko-ssh/SKILL.md) | `python`, `ssh`, `sftp`, `automation` |
| [`wordpress-themes`](skills/wordpress-themes/SKILL.md) | `php`, `wordpress`, `cms`, `frontend` |
| [`flet-desktop`](skills/flet-desktop/SKILL.md) | `python`, `desktop`, `flutter`, `gui` |
| [`sql-server`](skills/sql-server/SKILL.md) | `sql-server`, `t-sql`, `mssql`, `azure-sql` |
| [`db2-oracle`](skills/db2-oracle/SKILL.md) | `db2`, `oracle`, `plsql`, `enterprise` |
| [`salesforce-dev`](skills/salesforce-dev/SKILL.md) | `salesforce`, `apex`, `lwc`, `crm` |
| [`appian-lowcode`](skills/appian-lowcode/SKILL.md) | `appian`, `low-code`, `bpm` |
| [`prestashop-module`](skills/prestashop-module/SKILL.md) | `prestashop`, `php`, `e-commerce` |
| [`octane-alm`](skills/octane-alm/SKILL.md) | `octane`, `alm`, `defect-management` |

#### Content & Writing (2)

| Skill | Tags |
|-------|------|
| [`ebook-writer`](skills/ebook-writer/SKILL.md) | `ebook`, `writing`, `publishing`, `content` |
| [`prompt-engineering-best-practices`](skills/prompt-engineering-best-practices/SKILL.md) | `prompt-engineering`, `llm`, `cot`, `few-shot`, `role-prompting` |

### Agents

#### QA & Testing (7)

| Agent | Type |
|-------|------|
| [`test-architect`](agents/test-architect/agent.md) | `review` |
| [`qa-automation-engineer`](agents/qa-automation-engineer/agent.md) | `coding` |
| [`performance-tester`](agents/performance-tester/agent.md) | `research` |
| [`qa-lead`](agents/qa-lead/agent.md) | `governance` |
| [`api-tester`](agents/api-tester/agent.md) | `coding` |
| [`accessibility-tester`](agents/accessibility-tester/agent.md) | `review` |
| [`prompt-engineer`](agents/prompt-engineer/agent.md) | `review` |

#### Development (1)

| Agent | Type |
|-------|------|
| [`code-reviewer`](agents/code-reviewer/agent.md) | `review` |

#### Security (1)

| Agent | Type |
|-------|------|
| [`security-auditor`](agents/security-auditor/agent.md) | `governance` |

#### DevOps (1)

| Agent | Type |
|-------|------|
| [`devops-automator`](agents/devops-automator/agent.md) | `automation` |

### Prompts (64)

#### System / Task / Templates (9)

| Prompt | Type |
|--------|------|
| [`python-expert`](prompts/system/python-expert.md) | System |
| [`java-spring-expert`](prompts/system/java-spring-expert.md) | System |
| [`qa-engineer`](prompts/system/qa-engineer.md) | System |
| [`generate-api-tests`](prompts/task/generate-api-tests.md) | Task |
| [`refactor-legacy-code`](prompts/task/refactor-legacy-code.md) | Task |
| [`write-tech-documentation`](prompts/task/write-tech-documentation.md) | Task |
| [`create-docker-compose`](prompts/task/create-docker-compose.md) | Task |
| [`feature-file-template`](prompts/templates/feature-file-template.md) | Template |
| [`pull-request-template`](prompts/templates/pull-request-template.md) | Template |
| [`bug-report-template`](prompts/templates/bug-report-template.md) | Template |

#### QA Engineering (30)

| Prompt | Focus |
|--------|---------|
| [`generate-test-cases-from-requirements`](prompts/qa/generate-test-cases-from-requirements.md) | Test design |
| [`generate-api-test-suite`](prompts/qa/generate-api-test-suite.md) | API testing |
| [`generate-e2e-test-scenarios`](prompts/qa/generate-e2e-test-scenarios.md) | E2E / POM |
| [`analyze-bug-root-cause`](prompts/qa/analyze-bug-root-cause.md) | Bug analysis |
| [`generate-performance-test-plan`](prompts/qa/generate-performance-test-plan.md) | Performance |
| [`generate-security-test-cases`](prompts/qa/generate-security-test-cases.md) | Security / OWASP |
| [`generate-test-data`](prompts/qa/generate-test-data.md) | Data generation |
| [`generate-accessibility-test-checklist`](prompts/qa/generate-accessibility-test-checklist.md) | a11y / WCAG |
| [`generate-mobile-test-strategy`](prompts/qa/generate-mobile-test-strategy.md) | Mobile / Appium |
| [`generate-database-test-scenarios`](prompts/qa/generate-database-test-scenarios.md) | DB testing |
| [`generate-regression-test-suite`](prompts/qa/generate-regression-test-suite.md) | Regression |
| [`generate-ci-cd-quality-gates`](prompts/qa/generate-ci-cd-quality-gates.md) | Pipeline gates |
| [`generate-test-automation-strategy`](prompts/qa/generate-test-automation-strategy.md) | Automation ROI |
| [`review-test-code-quality`](prompts/qa/review-test-code-quality.md) | Test review |
| [`generate-load-test-script`](prompts/qa/generate-load-test-script.md) | k6 / Locust |
| [`generate-exploratory-test-charter`](prompts/qa/generate-exploratory-test-charter.md) | Exploratory |
| [`validate-user-story-testability`](prompts/qa/validate-user-story-testability.md) | INVEST / AC review |
| [`generate-compatibility-test-matrix`](prompts/qa/generate-compatibility-test-matrix.md) | Cross-browser |
| [`generate-test-summary-report`](prompts/qa/generate-test-summary-report.md) | Reporting |
| [`generate-data-migration-test-plan`](prompts/qa/generate-data-migration-test-plan.md) | Migration |
| [`generate-api-contract-test`](prompts/qa/generate-api-contract-test.md) | Pact / Schema |
| [`generate-canary-deployment-health-checks`](prompts/qa/generate-canary-deployment-health-checks.md) | Canary deploy |
| [`generate-observability-test-plan`](prompts/qa/generate-observability-test-plan.md) | Monitoring |
| [`generate-disaster-recovery-test-scenarios`](prompts/qa/generate-disaster-recovery-test-scenarios.md) | DR / Backup |
| [`generate-qa-interview-questions`](prompts/qa/generate-qa-interview-questions.md) | Hiring |
| [`generate-test-data-privacy-compliance`](prompts/qa/generate-test-data-privacy-compliance.md) | GDPR / HIPAA |
| [`generate-test-environment-setup-guide`](prompts/qa/generate-test-environment-setup-guide.md) | Environment |
| [`generate-flaky-test-diagnosis`](prompts/qa/generate-flaky-test-diagnosis.md) | Flakiness |
| [`generate-qa-metrics-dashboard`](prompts/qa/generate-qa-metrics-dashboard.md) | KPIs / DORA |
| [`generate-bdd-scenario`](prompts/qa/generate-bdd-scenario.md) | BDD / Gherkin |
| [`generate-visual-regression-test`](prompts/qa/generate-visual-regression-test.md) | Percy / Chromatic |
| [`generate-mutation-test`](prompts/qa/generate-mutation-test.md) | Pitest / Stryker |
| [`generate-qa-risk-analysis`](prompts/qa/generate-qa-risk-analysis.md) | Risk matrix |
| [`generate-test-data-strategy`](prompts/qa/generate-test-data-strategy.md) | Data masking / GDPR |
| [`generate-accessibility-audit`](prompts/qa/generate-accessibility-audit.md) | WCAG / axe |
| [`generate-chaos-engineering-tests`](prompts/qa/generate-chaos-engineering-tests.md) | Gremlin / Chaos Mesh |
| [`generate-api-fuzzing-scenarios`](prompts/qa/generate-api-fuzzing-scenarios.md) | Hypothesis / schemathesis |
| [`generate-shift-left-strategy`](prompts/qa/generate-shift-left-strategy.md) | Shift-left / TDD |
| [`generate-test-automation-roi-report`](prompts/qa/generate-test-automation-roi-report.md) | ROI / Business case |
| [`generate-canary-test-strategy`](prompts/qa/generate-canary-test-strategy.md) | Canary / Feature flags |

#### Ebook Writing (15)

| Prompt | Focus |
|--------|---------|
| [`generate-ebook-outline`](prompts/ebooks/generate-ebook-outline.md) | Structure and planning |
| [`research-topic-for-ebook`](prompts/ebooks/research-topic-for-ebook.md) | Content research |
| [`generate-ebook-title-options`](prompts/ebooks/generate-ebook-title-options.md) | Naming and titles |
| [`write-ebook-introduction`](prompts/ebooks/write-ebook-introduction.md) | Opening chapter |
| [`write-ebook-chapter`](prompts/ebooks/write-ebook-chapter.md) | Chapter drafting |
| [`write-ebook-conclusion`](prompts/ebooks/write-ebook-conclusion.md) | Closing chapter |
| [`edit-ebook-chapter`](prompts/ebooks/edit-ebook-chapter.md) | Revision and editing |
| [`generate-ebook-case-study`](prompts/ebooks/generate-ebook-case-study.md) | Real-world examples |
| [`generate-ebook-exercises`](prompts/ebooks/generate-ebook-exercises.md) | Learning reinforcement |
| [`format-ebook-for-export`](prompts/ebooks/format-ebook-for-export.md) | PDF/EPUB preparation |
| [`generate-ebook-marketing-copy`](prompts/ebooks/generate-ebook-marketing-copy.md) | Promotion and sales |
| [`review-ebook-consistency`](prompts/ebooks/review-ebook-consistency.md) | Quality checking |
| [`create-ebook-table-of-contents`](prompts/ebooks/create-ebook-table-of-contents.md) | TOC generation |
| [`create-ebook-reference-list`](prompts/ebooks/create-ebook-reference-list.md) | Bibliography |
| [`write-ebook-chapter-summary`](prompts/ebooks/write-ebook-chapter-summary.md) | Preview copy |

### Rules

#### Coding Standards (4)

| Rule | Category |
|------|-----------|
| [`python-coding-rules`](rules/coding/python-coding-rules.md) | Python |
| [`java-coding-rules`](rules/coding/java-coding-rules.md) | Java |
| [`javascript-coding-rules`](rules/coding/javascript-coding-rules.md) | JavaScript / TypeScript |
| [`sql-coding-rules`](rules/coding/sql-coding-rules.md) | SQL |

#### QA & Testing (7)

| Rule | Category |
|------|-----------|
| [`pr-review-checklist`](rules/review/pr-review-checklist.md) | General review |
| [`test-review-rules`](rules/review/test-review-rules.md) | Test quality |
| [`test-automation-rules`](rules/review/test-automation-rules.md) | E2E automation |
| [`performance-testing-rules`](rules/review/performance-testing-rules.md) | Performance |
| [`mobile-testing-rules`](rules/review/mobile-testing-rules.md) | Mobile |
| [`api-testing-rules`](rules/review/api-testing-rules.md) | API testing |
| [`prompt-quality-rules`](rules/review/prompt-quality-rules.md) | Prompt engineering |

#### Behavior (2)

| Rule | Category |
|------|-----------|
| [`response-format-rules`](rules/behavior/response-format-rules.md) | Formatting |
| [`response-language-rules`](rules/behavior/response-language-rules.md) | Language |

#### CI/CD (1)

| Rule | Category |
|------|-----------|
| [`ci-cd-testing-rules`](rules/review/ci-cd-testing-rules.md) | Pipeline testing |

### Workflows

#### DevOps & Deployment (6)

| Workflow | Purpose |
|----------|-----------|
| [`deploy-flask-app`](workflows/deploy-flask-app.md) | Docker + nginx + CI/CD deployment |
| [`deploy-spring-boot-app`](workflows/deploy-spring-boot-app.md) | JAR + K8s + health checks |
| [`gitlab-ci`](workflows/gitlab-ci.md) | Complete GitLab pipeline |
| [`bitbucket-pipelines`](workflows/bitbucket-pipelines.md) | Bitbucket pipeline |
| [`kubernetes-deploy`](workflows/kubernetes-deploy.md) | K8s manifests + Helm |
| [`onboard-new-project`](workflows/onboard-new-project.md) | Initial project setup |

#### QA & Testing (5)

| Workflow | Purpose |
|----------|-----------|
| [`setup-e2e-automation`](workflows/setup-e2e-automation.md) | Bootstrap E2E automation with CI/CD |
| [`performance-test-session`](workflows/performance-test-session.md) | Structured performance testing: SLA → script → execute → analyze |
| [`visual-regression-setup`](workflows/visual-regression-setup.md) | Configure Chromatic/Percy/Loki with baselines and CI |
| [`bug-triage`](workflows/bug-triage.md) | Structured bug triage process |
| [`qa-release-gate`](workflows/qa-release-gate.md) | Quality gate before production release |

#### Content (1)

| Workflow | Purpose |
|----------|-----------|
| [`create-ebook`](workflows/create-ebook.md) | Ebook creation pipeline |

#### Templates (2)

| Workflow | Purpose |
|----------|-----------|
| [`create-new-skill`](workflows/create-new-skill.md) | Bootstrap a skill from template |
| [`create-new-agent`](workflows/create-new-agent.md) | Bootstrap an agent from template |

### Tools

| Tool | Function |
|------|---------|
| [`validate-resource`](tools/validate-resource/README.md) | Validates frontmatter, kebab-case, placeholders |
| [`generate-skill-scaffold`](tools/generate-skill-scaffold/README.md) | Interactive CLI to create skills |
| [`sync-skills-to-cursor`](tools/sync-skills-to-cursor/README.md) | Copies skills to `.cursor/rules/` |
| [`sync-skills-to-claude`](tools/sync-skills-to-claude/README.md) | Copies skills to `.claude/agents/` |
| [`export-skills-to-md`](tools/export-skills-to-md/README.md) | Concatenates skills into a single markdown |
| [`check-dead-links`](tools/check-dead-links/README.md) | Scans broken URLs in `.md` |

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
