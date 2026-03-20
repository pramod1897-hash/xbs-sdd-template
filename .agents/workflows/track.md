---
description: Appends a timestamped audit trail entry to docs/tracking/TRACK.md. Auto-called after every workflow stage. Also invokable manually to add notes.
---

# /track — Audit Trail Workflow

Triggered by:
- Auto: called internally at end of every workflow (analysis, validate, decompose, plan, code, test, review)
- Manual: `/track PRJ-101 plan: "Confirmed JWT approach with architect — no DB OTP"`
- Natural language: *"track PRJ-101 code as done: used event sourcing"*

---

## Steps

### Step 1 — Parse Input
Extract:
- Feature ID: `PRJ-101` → maps to `PRJ-101-story` (or exact match in TRACK.md)
- Stage: the current workflow stage (auto) or explicitly provided (manual)
- Status: `✅ Done` (auto), or provided by caller
- Remark: provided by calling workflow OR by human in manual call

If remark not provided, auto-generate from the stage's outputs (see track-agent.md).

### Step 2 — Read TRACK.md
Read `docs/tracking/TRACK.md`. Find the section for this feature ID. If no section, create one.

### Step 3 — Append Entry
Add a new row to the feature's table:
```
| [Stage] | [YYYY-MM-DD HH:MM] | [actor] | [status] | [remark] |
```

### Step 4 — Save TRACK.md
Write the updated file.

### Step 5 — Confirm (no human gate)
Print:
```
📝 Tracked: PRJ-101-story / [Stage] → TRACK.md updated
```

---

## Manual Note Format
When called manually with a free-form note:
```
/track PRJ-101 code: "Architect approved using event sourcing over direct call"
```
Appended as:
```
| Code (note) | 2026-03-14 23:10 | human | 📝 Note | Architect approved event sourcing over direct call |
```

---

## View Tracking History
```
/track PRJ-101 --history
```
Displays the full table for PRJ-101 inline without modifying the file.
