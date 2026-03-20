---
description: Runs a full 5-dimension review (spec compliance, architecture, code quality, test coverage, non-functional) and produces review.md for human sign-off.
---

# /review — Review Workflow

Triggered by:
- `/review PRJ-101`
- *"review PRJ-101"* / *"check PRJ-101"* / *"is PRJ-101 ready?"*

---

## Pre-condition Check
If `docs/features/<id>/spec.md` is missing:
```
❌ spec.md not found. Complete /plan and /code before /review.
```

---

## Steps

### Step 1 — Load Full Context Bundle
Invoke context-loader for stage `/review` (all available files).

### Step 2 — Fetch PR Diff (if available)
Invoke mcp-bitbucket to check for a PR matching this Jira ID. If found, get diff summary.

### Step 3 — Run Spec Validator
```
node scripts/validate-spec.js docs/features/<id>/spec.md
```
Report result before full review.

### Step 4 — Invoke review-agent
Hand off to `review-agent.md` which performs the 5-dimension review:
1. **Spec Compliance** — AC × implemented × tested matrix
2. **Architecture** — boundary validation vs architecture.md
3. **Code Quality** — standards compliance vs standards.md
4. **Test Coverage** — AC coverage matrix, error paths, edge cases
5. **Non-Functional** — security, performance, observability, config

Writes: `docs/features/<id>/review.md`

### Step 5 — ⏸ HUMAN GATE
```
⏸ HUMAN GATE — /review
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📄 Created: docs/features/PRJ-101-story/review.md

❌ Violations (must fix): N
⚠️ Warnings (your call): M

Reply "proceed" → track as Done (after fixing violations)
Reply "fix [instruction]" → fix specific item then re-review
Reply "override [reason]" → proceed with violations (reason logged)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Step 6 — Auto-Track
Run the track command to log this stage:
`/track <jira-id> review: "0 violations; approved for merge"`

### Step 7 — Final Status
```
✅ /review complete — PRJ-101-story is APPROVED FOR MERGE

Summary:
  • 4/4 ACs implemented and tested
  • 0 architecture violations
  • 1 warning accepted (configurable token expiry)
  • review.md saved for audit trail
```
