---
name: Generate Exploratory Test Charter
version: 1.0.0
author: Mathias Paulenko Echeverz
description: Generate a session-based exploratory testing charter with mission, scope, risks, and note-taking template.
tags: [qa, exploratory-testing, charter, session-based, manual-testing]
role: qa-engineer
model: any
trigger: When the user asks for exploratory testing, test charters, session-based testing, or ad-hoc testing.
---

# Generate Exploratory Test Charter

Generate a session-based exploratory testing charter for a feature or area of the application.

## Charter Structure

### 1. Mission
What are we trying to learn or verify?

```
Explore the checkout flow to discover usability issues,
payment edge cases, and error handling gaps.
```

### 2. Scope

| In Scope | Out of Scope |
|----------|--------------|
| Guest checkout | Admin dashboard |
| Credit card payments | PayPal/Apple Pay |
| Error messages | Order fulfillment |
| Mobile responsive | Email notifications |

### 3. Risks & Oracles

- **User confusion**: Will users understand shipping options?
- **Data loss**: If browser crashes mid-checkout, is cart preserved?
- **Accessibility**: Can screen reader users complete checkout?
- **Performance**: Does checkout slow down with 50+ items?

### 4. Test Ideas

- [ ] Complete checkout as guest, registered user, and returning customer
- [ ] Enter invalid card numbers (Luhn fail, expired, wrong CVV)
- [ ] Change shipping address mid-checkout
- [ ] Apply expired/invalid promo codes
- [ ] Abandon checkout at each step, then return
- [ ] Use browser back/forward during checkout
- [ ] Open checkout in multiple tabs simultaneously

### 5. Session Notes Template

```markdown
## Session: [Date] [Time] [Tester]

### Environment
- Browser: Chrome 120
- OS: Windows 11
- Screen: 1920x1080

### Notes
| Time | Action | Observation | Issue? |
|------|--------|-------------|--------|
| 0:05 | Entered invalid ZIP | Error message unclear | ⚠️ Minor |
| 0:12 | Applied 2 promo codes | Second one overwrote first | 🔴 Bug |

### Issues Found
- [ ] BUG-001: Promo code stacking not handled
- [ ] OBS-001: ZIP error message needs improvement

### Coverage
- [x] Guest checkout
- [x] Registered checkout
- [ ] Mobile checkout (deferred)
```

## Best Practices

- Time-box sessions: 60-90 minutes max
- One charter per session
- Debrief after each session (what was learned)
- Pair testing for complex features
- Use mind maps for note-taking
