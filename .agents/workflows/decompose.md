---
description: Breaks a validated ticket into atomic, implementation-ready tasks using a strategy tailored to the ticket type (Epic/Story/Task/Bug/Sub-task).
---

# /decompose — Decomposition Workflow

Triggered by:
- `/decompose PRJ-101`
- *"break down PRJ-101"* / *"decompose story PRJ-101"* / *"split PRJ-101 into tasks"*

---

## Pre-condition Check
If `docs/features/<id>/context.md` does not exist:
```
❌ Run /analysis PRJ-101 and /validate PRJ-101 first.
```

---

## Steps

### Step 1 — Read Ticket Type
Read ticket type from `context.md` header: Epic / Story / Task / Bug / Sub-task.
Display:
```
📂 PRJ-101 detected as: Story
Using decomposition strategy: Story → Implementation Layers
```

### Step 2 — Invoke decompose-agent
Hand off to `decompose-agent.md` which:
- Loads context bundle (context-loader: stack, standards, context.md)
- Applies the ticket-type-specific decomposition strategy
- Builds AC coverage matrix per task
- Writes `docs/features/<id>/decompose.md`

### Step 3 — ⏸ HUMAN GATE
```
⏸ HUMAN GATE — /decompose
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📄 Created: docs/features/PRJ-101-story/decompose.md

Tasks proposed: 7 (Story path)
AC Coverage Matrix: 4 ACs mapped

Please review the task breakdown:
• Reorder tasks if needed (edit the file)
• Remove out-of-scope tasks
• Add missing tasks
• Adjust AC coverage mapping

Reply "proceed" → /plan
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Step 4 — Auto-Track
Run the track command to log this stage:
`/track <jira-id> decompose: "<N> tasks defined using <Story/Bug/Task> strategy"`
Remark summarizes task count, ticket type strategy, and any human adjustments.

### Step 5 — Suggest Next Step
```
✅ /decompose complete for PRJ-101-story (7 tasks)
Next: run /plan PRJ-101 to generate spec.md and plan.md
```
