---
name: context-loader
description: Stage-aware context bundle assembler. Reads and merges relevant context files at the start of every workflow stage, giving each agent exactly the right information — no more, no less.
---

# Context Loader Skill

## Purpose

**Context is everything.** The quality of every agent's output directly depends on having the right context at the right moment. This skill assembles a **context bundle** tailored to the current workflow stage.

Called at the **start of every workflow** before the agent does its work.

---

## How It Works

The context-loader reads sources **in this fixed priority order**, including only files that exist:

```
Priority  Source File                                    Stage Available
────────  ──────────────────────────────────────────    ──────────────────────────
  1       .agents/context/stack.md                      All stages
  2       .agents/context/standards.md                  All stages
  3       .agents/context/architecture.md               All stages
  4       docs/features/<id>/context.md                 After /analysis
  5       docs/features/<id>/spec.md                    After /plan
  6       docs/features/<id>/decompose.md               After /decompose
  7       docs/features/<id>/plan.md                    After /plan
  8       docs/tracking/TRACK.md (feature section)      After first /track call
```

Files that **do not yet exist** are silently skipped with a logged note.

---

## Stage-by-Stage Bundle

| Workflow Stage | Files Loaded | Why |
|---|---|---|
| `/analysis` | stack, standards, architecture | Tech context before fetching |
| `/validate` | + context.md | Validate against gathered info |
| `/decompose` | + context.md, stack | Decompose in tech context |
| `/plan` | + context.md, decompose.md, stack, standards | Plan with all business + tech info |
| `/code` | + context.md, spec.md, plan.md, stack, standards, architecture | Maximum context for code gen |
| `/test` | + spec.md, plan.md, stack, standards | AC-labelled tests need spec |
| `/review` | ALL available files | Full picture for sign-off |
| `/track` | None (write-only) | Just appends |

---

## Output

The context-loader produces a **context preamble** that is injected at the top of the agent's instruction before it works:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📦 CONTEXT BUNDLE — Stage: /code | Feature: PRJ-101-story
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[stack.md content]
────────────────
[standards.md content]
────────────────
[architecture.md content]
────────────────
[context.md content]
────────────────
[spec.md content]
────────────────
[plan.md content]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ℹ️  TRACK.md history: 4 previous stages completed for PRJ-101
⚠️  Missing: decompose.md (skipped — not available at this stage)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Learning from History

The context-loader also reads the **TRACK.md section for the current feature** to surface past decisions:

```
📜 Past decisions for PRJ-101-story:
  • Validate [2026-03-14]: "AC-2 reworded — email case-insensitive confirmed"
  • Plan [2026-03-14]: "JWT approach approved; no DB token storage"
```

This means every downstream agent **learns from earlier human decisions** in the same feature, preventing contradictions and repeated questions.

---

## Configuration

No configuration needed. The context-loader auto-discovers feature ID from:
1. The slash command argument: `/code PRJ-101`
2. The current directory: if running from `docs/features/PRJ-101-story/`
3. The last active feature in `TRACK.md`

---

## Error Handling

| Situation | Behaviour |
|---|---|
| `stack.md` missing | ⚠️ Warn human: "Fill in `.agents/context/stack.md` for best results" |
| `context.md` missing at `/code` | ❌ Block: "Run /analysis first before /code" |
| `spec.md` missing at `/test` | ❌ Block: "Run /plan first before /test" |
| All 3 context files missing | ⚠️ Warn but allow: "No team context files. Results may be generic." |
