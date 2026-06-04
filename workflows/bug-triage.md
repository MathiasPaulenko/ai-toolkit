---
name: Bug Triage
version: 1.0.0
author: Mathias Paulenko Echeverz
description: Structured bug triage process: intake, classification, prioritization, assignment, and resolution tracking. Ensures no bug falls through the cracks.
tags: [workflow, bug-triage, qa, process, defect-management]
role: qa-lead
---

# Bug Triage

Structured process for triaging incoming bugs efficiently.

## Prerequisites

- [ ] Triage meeting scheduled (daily or bi-daily)
- [ ] Team members: QA Lead, Dev Lead, Product Owner
- [ ] Triage board/dashboard ready (Jira, Azure DevOps, etc.)

## Phase 1: Intake & Reproduction

### Step 1: Verify Reproducibility

| Status | Action | Owner |
|--------|--------|-------|
| **Reproducible** | Proceed to classification | Reporter |
| **Intermittent** | Add logs, environment details | Reporter + QA |
| **Cannot reproduce** | Request more info, close after 3 days | QA |

### Step 2: Gather Context

```markdown
- [ ] Steps to reproduce documented
- [ ] Expected vs actual behavior stated
- [ ] Environment (browser, OS, version)
- [ ] Logs / screenshots / video attached
- [ ] Regression? (worked in version X)
```

## Phase 2: Classification

### Severity Matrix

| Severity | Definition | Example | SLA |
|----------|-----------|---------|-----|
| **P0 - Critical** | Production down, data loss, security breach | Cannot checkout, payment failing | 4 hours |
| **P1 - High** | Major feature broken, no workaround | Search returns no results | 1 day |
| **P2 - Medium** | Feature degraded, workaround exists | Slow page load, button misaligned | 1 week |
| **P3 - Low** | Cosmetic, minor inconvenience | Typo in error message | Next sprint |

### Component Assignment

```markdown
| Component | Auto-Assign | Escalation |
|-----------|-------------|------------|
| Frontend | UI Team | → Architecture if framework issue |
| Backend API | API Team | → Platform if infrastructure |
| Database | DB Team | → SRE if replication |
| Mobile | Mobile Team | → Native if OS-specific |
| Security | Security Team | → CISO if breach suspected |
```

## Phase 3: Prioritization

### Business Impact vs Engineering Effort

```
High Impact + Low Effort  → Do Now
High Impact + High Effort → Plan Next Sprint
Low Impact + Low Effort   → Backlog (quick wins)
Low Impact + High Effort  → Won't Fix / Icebox
```

### Triage Decision Record

```markdown
| Bug ID | Severity | Component | Decision | Owner | Due |
|--------|----------|-----------|----------|-------|-----|
| BUG-123 | P1 | Checkout | Fix this sprint | Alice | 2024-02-15 |
| BUG-124 | P2 | Search | Backlog | Bob | — |
| BUG-125 | P0 | Auth | Hotfix release | Carol | 2024-02-10 |
```

## Phase 4: Assignment & Tracking

### Step 1: Assign Owner
- P0/P1: Assign immediately in triage meeting
- P2: Assign during sprint planning
- P3: Pool in backlog, pick up during slack time

### Step 2: Set Due Dates

| Severity | Dev Start | Code Review | QA Verify | Release |
|----------|-----------|-------------|-----------|---------|
| P0 | Same day | Same day | Same day | Hotfix |
| P1 | Next day | +1 day | +1 day | Next release |
| P2 | This sprint | This sprint | This sprint | Next release |
| P3 | When picked | When picked | When picked | Next release |

## Phase 5: Resolution & Closure

### Closure Criteria

- [ ] Fix deployed to staging
- [ ] QA verifies fix in staging
- [ ] Regression test added (for P0/P1)
- [ ] Release notes updated
- [ ] Customer notified (if reported externally)

### Reopened Bugs

```markdown
If a "fixed" bug is reported again:
1. Reopen with new reproduction steps
2. Escalate severity by one level
3. Assign to original fixer + senior dev
4. Root cause analysis required
```

## Triage Meeting Agenda (15 min)

```markdown
1. New bugs since last triage (5 min)
   - Reproducibility status
   - Initial severity guess

2. Bug decisions (8 min)
   - Confirm/reclassify severity
   - Assign owners
   - Set due dates

3. Metrics review (2 min)
   - Open bug count by severity
   - Average age of open bugs
   - Bugs reopened this week
```

## Verification Checklist

- [ ] Triage meeting scheduled and attended
- [ ] Every new bug has severity + owner within 24h
- [ ] P0 bugs have SLA timer started
- [ ] Dashboard shows aging bugs > 7 days
- [ ] Weekly metrics reviewed with team
