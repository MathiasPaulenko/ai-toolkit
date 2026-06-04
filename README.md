# ai-toolkit

Repositorio personal de recursos de IA: prompts, skills, agents, rules, workflows y herramientas creados para obtener resultados consistentes y estructurados con LLMs.

## Recursos (83)

| Categoría | Cantidad |
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

| Prompt | Tipo |
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

| Prompt | Enfoque |
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

| Rule | Categoría |
|------|-----------|
| `python-coding-rules` | Coding |
| `java-coding-rules` | Coding |
| `javascript-coding-rules` | Coding |
| `sql-coding-rules` | Coding |
| `pr-review-checklist` | Review |
| `test-review-rules` | Review |
| `response-format-rules` | Behavior |
| `bilingual-rules` | Behavior |

### Workflows

| Workflow | Propósito |
|----------|-----------|
| `create-new-skill` | Bootstrap de skill desde template |
| `create-new-agent` | Bootstrap de agent desde template |
| `deploy-flask-app` | Despliegue Docker + nginx + CI/CD |
| `deploy-spring-boot-app` | JAR + K8s + health checks |
| `gitlab-ci` | Pipeline GitLab completa |
| `bitbucket-pipelines` | Pipeline Bitbucket |
| `kubernetes-deploy` | Manifiestos K8s + Helm |
| `onboard-new-project` | Setup inicial de proyecto |

### Tools

| Tool | Función |
|------|---------|
| `validate-resource` | Valida frontmatter, kebab-case, placeholders |
| `generate-skill-scaffold` | CLI interactivo para crear skills |
| `sync-skills-to-cursor` | Copia skills a `.cursor/rules/` |
| `sync-skills-to-claude` | Copia skills a `.claude/agents/` |
| `export-skills-to-md` | Concatena skills en un solo markdown |
| `check-dead-links` | Escanea URLs rotas en `.md` |

## Estructura

| Carpeta | Contenido |
|---------|-----------|
| `prompts/` | Prompts de sistema, tareas y plantillas reutilizables |
| `skills/` | Skills estructurados con `SKILL.md` y assets |
| `agents/` | Definiciones de agentes (`agent.md`, knowledge, tools) |
| `rules/` | Reglas de código, revisión y comportamiento |
| `workflows/` | Procedimientos paso a paso para flujos repetitivos |
| `tools/` | Utilidades, scripts y recursos técnicos |
| `AGENTS.md` | Estándares y convenciones globales del repositorio |
| `justfile` | Comandos comunes (`just validate`, `just export`, etc.) |
| `.devin/` | Workflows específicos para Devin |
| `.cursor/` | Reglas y prompts para Cursor |

## Convenciones

- Cada recurso va en su carpeta con nombre en `kebab-case`
- Skills y agents llevan un `README.md` o `SKILL.md` / `agent.md`
- Se usa frontmatter YAML para metadatos (autor, versión, tags, trigger)
- Material de referencia técnica va en `references/`; ejecutables y plantillas en `assets/`
- Las plantillas de ejemplo están en `_template/` dentro de cada categoría

## Uso rápido

Copiar el recurso deseado al contexto del modelo o referenciarlo desde la configuración del IDE (Cursor Rules, Devin Workflows, etc).

## Comandos

```bash
# Validar todos los recursos
just validate

# Generar skill nuevo (interactivo)
just generate-skill

# Exportar skills a markdown
just export

# Verificar links rotos
just check-links

# Ejecutar todas las validaciones
just check
```

## Licencia

Este proyecto está licenciado bajo [MIT](LICENSE).

Para uso comercial o empresarial, consulta las expectativas de atribución en [NOTICE.md](NOTICE.md).

Copyright (c) 2026 Mathias Paulenko Echeverz
