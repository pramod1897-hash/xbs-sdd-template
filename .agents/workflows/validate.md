---
description: Validates the gathered context and Acceptance Criteria for quality, testability, and completeness before allowing decomposition.
---

# /validate — Validation Workflow

Triggered by:
- `/validate PRJ-101`
- *"validate story PRJ-101"* / *"check ACs for PRJ-101"*

---

## Pre-condition Check
If `docs/features/<id>/context.md` does not exist:
```
❌ context.md not found for PRJ-101.
Run /analysis PRJ-101 first, then re-run /validate.
```

---

## Steps

### Step 1 — Load context.md
Read `docs/features/<id>/context.md` produced by `/analysis`.

### Step 2 — Invoke validate-agent
Hand off to `validate-agent.md` which:
- Loads context bundle (context-loader: stack, standards, context.md)
- Runs spec-validator Layer 2 (AC quality check)
- Runs `node scripts/validate-spec.js` if spec.md exists
- Produces validation report in-line

### Step 3 — ⏸ HUMAN GATE
```
⏸ HUMAN GATE — /validate
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Validation report displayed here]

REQUIRED fixes before proceeding: N
WARNINGS (your call): M

Reply "proceed" → /decompose (after fixing required items)
Reply "skip [reason]" → proceed without fixing (adds override note to TRACK.md)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Step 4 — Auto-Track
Run the track command to log this stage:
`/track <jira-id> validate: "Context validated; <N> ACs"`

### Step 5 — Suggest Next Step
```
✅ /validate complete for PRJ-101-story
Next: run /decompose PRJ-101 to break into implementation tasks
```
