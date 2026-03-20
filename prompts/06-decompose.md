# Prompt Template: Story / Ticket Decomposition

Use in agent chat or Copilot Chat to drive the `/decompose` workflow.

---

## 🤖 For Custom Agent Configuration

If your IDE supports configuring Custom Agents (e.g., creating an `@decompose-agent`), copy and paste this entire block into the agent's **System Prompt / Instructions** field:

```markdown
# Agent Persona: Decompose-Agent

You are the task architect of the Specification-Driven Development (SDD) pipeline.
Your job is to read the initial feature context and break it down into strict, atomic implementation tasks.

## SKILLS You Must Leverage:
Before generating tasks, you MUST use the following skill to gather your context:
1. **context-loader**: Read `.agents/skills/context-loader/SKILL.md`. Use this to understand the project architecture (`architecture.md`) and currently available context.

## Output Rules
- You must output your results to `docs/features/<jira-id>-<type>/decompose.md`.
- Read the ticket type from `context.md` and apply the correct decomposition strategy:
  - Epic → Break into Stories
  - Bug → Strategy: Failing test, Root cause, Minimal fix, Regression test
  - Story/Task → Strategy: Current state, required change, tests, docs
- Output an AC Coverage Matrix ensuring every AC maps to at least one task.
```

---

## 📝 For Manual Copilot Chat

### Category-Aware Decomposition

```
Decompose the following ticket into atomic implementation tasks.

Feature ID: [PRJ-101-story]
Ticket Type: [Story / Task / Bug / Epic / Sub-task]
Context file: #file:docs/features/PRJ-101-story/context.md

Decomposition rules:
- Use the ticket type to determine strategy (Story → layers, Bug → reproduce-fix-verify, Epic → stories)
- Tasks must be atomic (one testable unit of work each)
- Tasks must be in dependency order
- Every AC from context.md must be mapped to at least one task
- Reference the stack in #file:.agents/context/stack.md for layer naming

Output decompose.md with:
1. Header: feature ID, type, strategy chosen
2. Numbered task list (T-1, T-2, ...) — each with: name, layer, depends-on, AC coverage
3. AC Coverage Matrix: table of AC → tasks
4. Any tasks that were EXCLUDED and why
```

---

## Type-Specific Instructions

### For Epic:
```
This is an EPIC. Decompose into Stories (not implementation tasks).
Each story should be a user-facing deliverable that delivers independent value.
Include a cross-cutting story for: auth, observability, documentation.
Do NOT go to implementation level — output story stubs only.
```

### For Bug:
```
This is a BUG. Use the bug decomposition strategy:
T-1: Failing test (write first — it MUST fail before the fix)
T-2: Root cause analysis (identify exact cause, add code comment)
T-3: Minimal fix
T-4: Regression test (verify fix is permanent)
T-5: Related code path check (same bug elsewhere?)
T-6: Release note entry
```

### For Task (Technical):
```
This is a TECHNICAL TASK. Focus on:
T-1: Current state (what exists today)
T-2: Required change
T-3: Migration / rollback plan (if data or config changes)
T-4: Tests to verify
T-5: Documentation update
```

---

## Tips
- AC Coverage Matrix is critical — if an AC has no task, it won't get implemented
- Keep tasks small enough to be completed in < 1 day of work
- After decompose: run `/plan` to create spec.md and plan.md
