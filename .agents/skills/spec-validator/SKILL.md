---
name: spec-validator
description: Validates a spec.md file using the scripts/validate-spec.js linter and performs an AI-level Acceptance Criteria quality check. Reports all issues clearly for human review.
---

# Spec Validator Skill

## Purpose
Two-layer spec validation:
1. **Structural** — run `scripts/validate-spec.js` (linter)
2. **Quality** — AI check that each AC is testable, unambiguous, and complete

Used in `/validate` and `/plan` workflows.

---

## Layer 1 — Structural Validation (Script)

### How to Run

```bash
node scripts/validate-spec.js docs/features/<jira-id>-<type>/spec.md
```

### What It Checks
- Required sections present: `## Inputs`, `## Outputs`, `## Business Rules`, `## Acceptance Criteria`
- At least 1 AC exists in `AC-N:` format
- No empty sections

### Interpreting Output
- `✅ SPEC VALID` → proceed to Layer 2
- `❌ SPEC INVALID` → list failures, do NOT proceed; surface to human

---

## Layer 2 — AC Quality Check (AI)

For every Acceptance Criterion, evaluate against these criteria:

### Testability Check
Each AC must follow **Given / When / Then** (or be convertible to it):
- ✅ PASS: "Given a registered user, When they request a reset, Then an email is sent within 30s"
- ❌ FAIL: "The system should send emails quickly" — too vague

### Completeness Check
Each AC must specify:
- [ ] The actor (who)
- [ ] The trigger (what action)
- [ ] The expected outcome (what result)
- [ ] Error/edge case handling (if applicable)

### Non-Duplication Check
Flag any two ACs that test the same behaviour.

### Conflict Check
Flag any two ACs that contradict each other.

---

## Output Format

```markdown
## Spec Validation Report

### Layer 1 — Structural (validate-spec.js)
✅ All required sections present
✅ 4 ACs found
⚠️ Business Rules section is sparse (1 rule) — consider adding more

### Layer 2 — AC Quality

| AC | Testable | Complete | Issues |
|----|----------|----------|--------|
| AC-1 | ✅ | ✅ | — |
| AC-2 | ⚠️ | ✅ | Missing error case: what if email not found? |
| AC-3 | ❌ | ❌ | "system should handle it gracefully" — needs rewrite |

### Required Changes Before Proceeding
- [ ] AC-2: Add error case for unregistered email
- [ ] AC-3: Rewrite as Given/When/Then
```

---

## Human Gate

After producing the validation report:
```
⏸ HUMAN GATE — /validate
Please review the spec validation report above.
- Fix the flagged ACs in spec.md (or update the Jira ticket)
- Reply "proceed" when all issues are resolved (or "skip" to override with justification)
```
