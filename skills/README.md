# Skills

Reusable domain guides that follow the repository conventions.
Each skill provides focused guidance, best practices, examples,
and references for a specific tool, framework, or workflow.

## Format

Each skill is a folder named in `kebab-case` containing at least
a `SKILL.md` file with this structure:

```markdown
---
name: Skill Name
version: 1.0.0
author: Mathias Paulenko Echeverz
description: One-line value proposition
tags: [tag1, tag2, tag3]
trigger: When the user asks about...
---

# Skill Name

## Description

Brief explanation of what the skill covers.

## Usage

### When to invoke

- ...

## References

- Links to related resources
```

Extended material goes in `references/` and executable templates
in `assets/`.

## Skills by Category

### Content & Writing (2)

| Skill | Description | Tags |
| --- | --- | --- |
| [`ebook-writer`](skills/ebook-writer/SKILL.md) | Comprehensive ebook creation skill covering outlining, chapter writing, editing, formatting, and marketing. Supports technical, educational, and narrative ebooks. | `ebook, writing, publishing, content, long-form` |
| [`prompt-engineering-best-practices`](skills/prompt-engineering-best-practices/SKILL.md) | Best practices for designing high-quality prompts: Chain-of-Thought, Few-shot, Role Prompting, Self-Consistency, and output structuring. Apply to system, task, and template prompts. | `prompt-engineering, llm, cot, few-shot, role-prompting` |

### Development (12)

| Skill | Description | Tags |
| --- | --- | --- |
| [`android-native`](skills/android-native/SKILL.md) | Production-grade skill for native Android development with Jetpack Compose, MVVM, Hilt, Room, and Compose Navigation. Covers project setup, UI, architecture, DI, persistence, networking, and testing. | `android, kotlin, jetpack-compose, mvvm, mobile, native` |
| [`appian-lowcode`](skills/appian-lowcode/SKILL.md) | Appian low-code platform development guide. Covers process models, SAIL interfaces, data stores, expressions, integrations, and deployment best practices. | `appian, low-code, bpm, process-model, sail, enterprise` |
| [`db2-oracle`](skills/db2-oracle/SKILL.md) | Enterprise database development for IBM DB2 and Oracle. Covers PL/SQL, SQL/PL, partitioning, performance tuning, XML/JSON handling, and migration patterns. | `db2, oracle, plsql, database, enterprise, partitioning` |
| [`flask-api`](skills/flask-api/SKILL.md) | Production-grade skill for building REST APIs with Flask. Covers app factory, blueprints, extensions, configuration, testing, serialization, error handling, pagination, Docker, and deployment. | `flask, python, rest-api, backend, microservices, web` |
| [`flet-desktop`](skills/flet-desktop/SKILL.md) | Desktop application development with Flet (Flutter-based Python). Covers UI layout, state management, navigation, file handling, packaging, and cross-platform distribution. | `flet, python, desktop, flutter, gui, cross-platform, pyinstaller` |
| [`jinja2-templates`](skills/jinja2-templates/SKILL.md) | Production-grade skill for Jinja2 templating in Python. Covers syntax, inheritance, macros, filters, tests, escaping, security (autoescape, XSS), Flask/FastAPI integration, and standalone code generation. | `jinja2, templates, python, flask, fastapi, html, security` |
| [`octane-alm`](skills/octane-alm/SKILL.md) | Micro Focus ALM Octane integration guide. Covers REST API, entity management, defect tracking, test automation integration, and CI/CD pipeline reporting. | `octane, alm, testing, defect-management, rest-api, ci-cd` |
| [`paramiko-ssh`](skills/paramiko-ssh/SKILL.md) | SSH automation with Paramiko. Covers connection handling, command execution, file transfer (SFTP), key-based auth, bastion hosts, and async patterns for remote server management. | `python, ssh, paramiko, sftp, remote, automation, devops` |
| [`prestashop-module`](skills/prestashop-module/SKILL.md) | PrestaShop module development guide. Covers module structure, hooks, controllers, database schemas, payment modules, and overrides in PHP/Smarty. | `prestashop, php, e-commerce, module, cms, payment` |
| [`salesforce-dev`](skills/salesforce-dev/SKILL.md) | Salesforce development guide. Covers Apex triggers, Lightning Web Components (LWC), SOQL, SOSL, platform events, and deployment via SFDX. | `salesforce, apex, lwc, soql, sfdx, crm` |
| [`sql-server`](skills/sql-server/SKILL.md) | Microsoft SQL Server development guide. Covers T-SQL syntax, stored procedures, indexing strategies, temporal tables, JSON support, Always Encrypted, and Azure SQL specifics. | `sql-server, t-sql, mssql, database, azure-sql, stored-procedures` |
| [`wordpress-themes`](skills/wordpress-themes/SKILL.md) | WordPress theme development standards. Covers theme structure, template hierarchy, custom post types, ACF integration, enqueueing assets, security, and performance best practices. | `wordpress, php, theme, cms, frontend, acf` |

### SEO (4)

| Skill | Description | Tags |
| --- | --- | --- |
| [`google-crawling-indexing`](skills/google-crawling-indexing/SKILL.md) | Practical guide to Google crawling and indexing: sitemaps, robots.txt, meta tags, canonical URLs, redirects, JavaScript, removals, and crawler management. | `google-search, crawling, indexing, robots-txt, sitemaps` |
| [`google-ranking-appearance`](skills/google-ranking-appearance/SKILL.md) | Practical guide to Google search ranking and appearance: title links, snippets, structured data, rich results, images, videos, Discover, and local features. | `google-search, ranking, search-appearance, structured-data, rich-results` |
| [`google-seo-fundamentals`](skills/google-seo-fundamentals/SKILL.md) | Practical guide to Google Search SEO fundamentals: Search Essentials, technical requirements, spam policies, helpful content, generative AI guidelines, and site maintenance. | `google-search, seo-fundamentals, search-essentials, helpful-content, ai-seo` |
| [`google-seo-monitoring`](skills/google-seo-monitoring/SKILL.md) | Practical guide to Google SEO monitoring and debugging: Search Console, Google Analytics, Google Trends, search operators, traffic drops, security, spam, and malware. | `google-search, search-console, google-analytics, google-trends, monitoring` |

### Testing & QA (13)

| Skill | Description | Tags |
| --- | --- | --- |
| [`allure-reports`](skills/allure-reports/SKILL.md) | Production-grade skill for generating rich test reports with Allure. Covers pytest, Behave, JUnit, annotations, attachments, steps, CI/CD integration, and custom categories. | `allure, reporting, pytest, behave, junit, testing, ci-cd` |
| [`appium-mobile`](skills/appium-mobile/SKILL.md) | Mobile automation with Appium: iOS and Android, gestures, device farms (BrowserStack, Sauce Labs), parallel execution, and CI/CD. | `mobile, appium, ios, android, automation` |
| [`behave-bdd`](skills/behave-bdd/SKILL.md) | Production-grade skill for BDD testing with Python Behave (v1.3.0+). Covers Gherkin, step implementations, environment hooks, fixtures, tags, data tables, scenario outlines, formatters, and CI/CD integration. | `behave, bdd, python, testing, gherkin, e2e, cucumber` |
| [`jmeter-load-testing`](skills/jmeter-load-testing/SKILL.md) | Load and performance testing with Apache JMeter. Covers test plan design, thread groups, samplers, assertions, listeners, distributed testing, and CI/CD integration. | `jmeter, load-testing, performance, stress-test, jmx, ci-cd` |
| [`k6-load-testing`](skills/k6-load-testing/SKILL.md) | Modern load testing with k6: JavaScript scripting, Grafana dashboards, cloud execution, thresholds, extensions, and CI/CD integration. | `load-testing, k6, performance, grafana, javascript` |
| [`karate-api-testing`](skills/karate-api-testing/SKILL.md) | API testing with Karate DSL: REST, GraphQL, gRPC, mocking, parallel execution, CI/CD integration, and data-driven tests. | `api-testing, karate, bdd, rest, graphql` |
| [`postman-api-automation`](skills/postman-api-automation/SKILL.md) | API testing and automation with Postman/Newman: collections, environments, pre/post scripts, CI/CD reporting, and data-driven testing. | `api-testing, postman, newman, automation, rest` |
| [`pytest-advanced`](skills/pytest-advanced/SKILL.md) | Advanced pytest patterns: parametrization, fixtures (session/module/function), conftest.py, plugins (cov, xdist, mock), markers, and CI integration. | `pytest, python, testing, fixtures, plugins` |
| [`robot-framework`](skills/robot-framework/SKILL.md) | Production-grade skill for Robot Framework keyword-driven testing. Covers project structure, keywords, variables, libraries (Selenium, Requests, Database), resources, setup/teardown, tags, CLI execution, and CI/CD integration. | `robot-framework, testing, keyword-driven, automation, qa, selenium` |
| [`sonarqube-quality-gates`](skills/sonarqube-quality-gates/SKILL.md) | SonarQube quality gate configuration, coverage rules, custom profiles, and CI/CD integration for maintaining code quality across projects. | `sonarqube, quality-gates, static-analysis, code-quality, ci-cd, devops` |
| [`testcontainers`](skills/testcontainers/SKILL.md) | Integration testing with Testcontainers: PostgreSQL, Redis, Kafka, RabbitMQ, localstack. Spin up real dependencies in Docker for reliable integration tests. | `integration-testing, testcontainers, docker, databases, kafka` |
| [`webdriverio`](skills/webdriverio/SKILL.md) | WebdriverIO for E2E testing: Page Object Model, selectors, cross-browser execution, mobile emulation, visual regression, and CI/CD integration. | `e2e, webdriverio, selenium, automation, cross-browser` |
| [`xctest-ios`](skills/xctest-ios/SKILL.md) | Native iOS testing with XCTest: unit tests, UI automation, performance, snapshot testing, parallel execution, and CI/CD with Xcode Cloud. | `ios, xctest, swift, mobile, unit-testing` |

### Wave Ecosystem (13)

| Skill | Description | Tags |
| --- | --- | --- |
| [`bidiwave-cross-browser`](skills/bidiwave-cross-browser/SKILL.md) | Cross-browser testing with bidiwave using the W3C WebDriver BiDi protocol. Works with Chrome, Firefox, and Edge. RemoteValue pattern matching, preload scripts, web extensions, CDP bridge. | `webdriver-bidi, cross-browser, w3c, firefox-chrome` |
| [`bidiwave-network-interception`](skills/bidiwave-network-interception/SKILL.md) | Network interception with bidiwave. Block requests, modify requests, mock responses, auth handling, cache control, response body retrieval. | `network-interception, bidi, mocking, request-modification` |
| [`cdpwave-debugging`](skills/cdpwave-debugging/SKILL.md) | Advanced debugging with cdpwave. Breakpoints, step debugging, CPU profiling, heap snapshots, code coverage, DOM debugger. | `debugging, breakpoints, profiling, heap-snapshot` |
| [`cdpwave-testing`](skills/cdpwave-testing/SKILL.md) | Write browser automation tests with cdpwave at the CDP level. Async test patterns, multi-tab sessions, event handling, screenshots in CI, escape hatch for uncovered CDP methods. | `cdp, browser-testing, python-async, chrome-devtools` |
| [`wave-ecosystem-guide`](skills/wave-ecosystem-guide/SKILL.md) | Guide to the Wave browser automation ecosystem: cdpwave (CDP client), bidiwave (WebDriver BiDi client), wavexis (CLI), and wavexis-mcp (MCP server). Helps choose the right tool for each use case. | `wave-ecosystem, browser-automation, cdp, webdriver-bidi, mcp` |
| [`wavexis-accessibility`](skills/wavexis-accessibility/SKILL.md) | Accessibility auditing with wavexis. a11y tree snapshots, axe-core audits, node traversal, CI gates for WCAG compliance. | `accessibility, a11y, wcag, axe-core` |
| [`wavexis-ci-cd`](skills/wavexis-ci-cd/SKILL.md) | Integrate wavexis into CI/CD pipelines. CI assertions, visual regression, screenshots in PRs, deploy gates with CWV budgets, Docker serve mode. | `ci-cd, assertions, visual-diff, github-actions` |
| [`wavexis-cli-automation`](skills/wavexis-cli-automation/SKILL.md) | Browser automation with wavexis CLI: screenshots, PDFs, scraping, REPL, multi-action YAML, stealth mode, serve mode, performance audits, and CI assertions. 130+ commands, CDP + BiDi backends. | `wavexis, cli-automation, browser-automation, screenshot, scraping` |
| [`wavexis-mcp-agent-integration`](skills/wavexis-mcp-agent-integration/SKILL.md) | MCP server integration for LLM browser automation: 220 tools, 13 capability tiers, session management, natural language interaction, multi-action workflows, and IDE configuration for Claude, Cursor, Windsurf, and VS Code. | `wavexis-mcp, mcp-server, llm-integration, browser-automation, ai-agent` |
| [`wavexis-network-testing`](skills/wavexis-network-testing/SKILL.md) | Network testing with wavexis. HAR capture, request interception, response mocking, network throttling, WebSocket inspection, request modification. | `network, har, interception, mocking, throttling` |
| [`wavexis-performance-audit`](skills/wavexis-performance-audit/SKILL.md) | Performance auditing with wavexis. Core Web Vitals measurement (LCP, CLS, INP), CPU traces, JS/CSS coverage, heap snapshots, Lighthouse audits, CI budgets. | `core-web-vitals, performance, lighthouse, tracing` |
| [`wavexis-session-recording`](skills/wavexis-session-recording/SKILL.md) | Record and replay browser sessions with wavexis. Interactive recording, YAML session format, replay in CI. | `record-replay, session, yaml, automation` |
| [`wavexis-web-scraping`](skills/wavexis-web-scraping/SKILL.md) | Web scraping with wavexis. Stealth mode for anti-bot sites, crawl command for multi-page scraping, natural language selectors, shadow DOM scraping, batch processing. | `web-scraping, stealth, crawl, data-extraction` |

## Installation

Use the `skills.sh` script to install all skills into your IDE
skills directory:

```bash
bash tools/skills.sh
```

## Validation

Run the resource validator to check frontmatter and conventions:

```bash
python tools/validate-resource/validate.py
```
