---
description: Generates the formal spec.md and plan.md from validated context and decomposed tasks. Validates spec before human review.
---

# /plan — Planning Workflow

Triggered by:
- `/plan PRJ-101`
- *"plan PRJ-101"* / *"create spec for PRJ-101"* / *"write plan for PRJ-101"*

---

## Pre-condition Check
If `docs/features/<id>/decompose.md` does not exist:
```
❌ Run /decompose PRJ-101 first before /plan.
```

---

## Steps

### Step 1 — Load Accumulated Context
Invoke context-loader for stage `/plan`: reads stack, standards, architecture, context.md, decompose.md, TRACK.md history.

### Step 2 — Invoke plan-agent
Hand off to `plan-agent.md` which:
- Generates `docs/features/<id>/spec.md` from context.md ACs + business rules
- Validates spec: `node scripts/validate-spec.js docs/features/<id>/spec.md`
- Generates `docs/features/<id>/plan.md` with technical task sequence
- References `stack.md` for all tech-specific decisions

### Step 3 — Auto-Fix Structural Issues
If validate-spec.js reports structural errors, fix them automatically (missing sections, formatting).
Do NOT auto-fix AC content — flag for human.

### Step 4 — ⏸ HUMAN GATE
```
⏸ HUMAN GATE — /plan
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📄 Created: docs/features/PRJ-101-story/spec.md  (validator: ✅ VALID)
📄 Created: docs/features/PRJ-101-story/plan.md

Please review:
1. Business Rules — all captured from Jira/Confluence?
2. ACs — correct Given/When/Then form?
3. Plan — task sequence correct? Any risks missing?
4. "Not In Scope" section — anything wrongly excluded?

Reply "proceed" → /code
Reply "revise [what]" → update and re-validate before proceeding
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Step 5 — Auto-Track
Run the track command to log this stage:
`/track <jira-id> plan: "spec.md validated; technical implementation planned"`

### Step 6 — Suggest Next Step
```
✅ /plan complete — spec.md validated ✅
Next: run /code PRJ-101 to generate the implementation
```
