---
description: Generates production-quality source code from spec.md and plan.md using the full context bundle (stack, standards, architecture, Bitbucket patterns).
---

# /code — Code Generation Workflow

Triggered by:
- `/code PRJ-101`
- *"generate code for PRJ-101"* / *"implement PRJ-101"* / *"code PRJ-101"*

---

## Pre-condition Check
If `docs/features/<id>/spec.md` or `docs/features/<id>/plan.md` do not exist:
```
❌ Run /plan PRJ-101 first to generate spec.md and plan.md before /code.
```

---

## Steps

### Step 1 — Load Full Context Bundle
Invoke context-loader for stage `/code` (maximal bundle: all 7 sources).
Display what was loaded:
```
📦 Context bundle loaded:
  ✅ stack.md | ✅ standards.md | ✅ architecture.md
  ✅ context.md | ✅ spec.md | ✅ plan.md
  ✅ TRACK.md (5 prior decisions read)
```
If stack.md is missing, warn: `⚠️ stack.md is empty — fill in .agents/context/stack.md for best results`

### Step 2 — Fetch Codebase Style Reference
Invoke mcp-bitbucket to fetch 1 existing service file + 1 test file as style references.

### Step 3 — Invoke code-agent
Hand off to `code-agent.md` which:
- Reads tech stack from stack.md (language, framework, libraries)
- Reads standards from standards.md (patterns, anti-patterns)
- Reads boundaries from architecture.md
- Generates code task-by-task (T-1, T-2, T-3... from plan.md)
- After each file: states which ACs/BRs it implements

### Step 4 — ⏸ HUMAN GATE
```
⏸ HUMAN GATE — /code
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Generated files:
  • [file list with paths]

Context applied:
  • Tech: [stack.md summary]
  • Standards: [standards.md key rules]
  • Architecture: [boundaries respected]
  • Style ref: [Bitbucket file used]

Focus your review on:
1. Business rule correctness (vs spec.md)
2. Architecture boundary compliance (vs architecture.md)
3. Standards compliance (vs standards.md)

Reply "proceed" → /test
Reply "fix [instruction]" → targeted fix then re-present
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Step 5 — Auto-Track
Run the track command to log this stage:
`/track <jira-id> code: "<N> files generated adhering to architecture and standards"`

### Step 6 — Suggest Next Step
```
✅ /code complete — [N] files generated
Next: run /test PRJ-101 to generate and run AC-labelled tests
```
