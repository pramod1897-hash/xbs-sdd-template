# 🚀 SDD Workflow — Getting Started Guide

> **Specification-Driven Development (SDD)** enhanced with AI agents, MCP integrations, and human-gated workflows.  
> Works with **any tech stack**. AI assists — humans lead.

---

## The Core Idea

Traditional dev: *write code → hope it matches requirements → scramble at review time*  
SDD approach: *understand fully → validate → plan → generate → verify → track*

```
/analysis → /validate → /decompose → /plan → /code → /test → /review → (auto /track)
```

Every phase produces an artifact. Every phase awaits your approval before proceeding.

---

## Quick Start (5 Minutes)

### Step 1 — Fill In Your Project Context (Once Per Project)

These three files tell every agent about your project. Without them, agents still work but produce generic output.

| File | What to Fill In |
|------|----------------|
| [`.agents/context/stack.md`](.agents/context/stack.md) | Language, framework, libraries, test runner |
| [`.agents/context/standards.md`](.agents/context/standards.md) | Coding patterns, anti-patterns, naming rules |
| [`.agents/context/architecture.md`](.agents/context/architecture.md) | Module/service map and boundary rules |

> 💡 Fill these in once for your project — all 8 workflow stages will read them automatically.

### Step 2 — Start a Feature

With a Jira ticket (e.g. `PRJ-101`):

```
/analysis PRJ-101
```

Or with natural language:
```
analyse story PRJ-101 for me
```

### Step 3 — Follow the Pipeline

The agent will suggest the next step at the end of each stage. Just follow it:

```
✅ /analysis done → run /validate PRJ-101
✅ /validate done → run /decompose PRJ-101
✅ /decompose done → run /plan PRJ-101
✅ /plan done → run /code PRJ-101
✅ /code done → run /test PRJ-101
✅ /test done → run /review PRJ-101
```

---

## All Workflow Commands

| Command | What it does | Output |
|---------|-------------|--------|
| `/analysis PRJ-101` | Fetches Jira + Confluence + Bitbucket context | `docs/features/PRJ-101-story/context.md` |
| `/validate PRJ-101` | Quality-checks ACs for testability + completeness | Validation report |
| `/decompose PRJ-101` | Breaks ticket into typed atomic tasks | `docs/features/PRJ-101-story/decompose.md` |
| `/plan PRJ-101` | Generates spec.md + plan.md, validates spec | `spec.md`, `plan.md` |
| `/code PRJ-101` | Generates code using full context bundle | Source files |
| `/test PRJ-101` | Generates AC-labelled tests, runs them | Test files |
| `/review PRJ-101` | 5-dimension review → review.md | `docs/features/PRJ-101-story/review.md` |
| `/track PRJ-101` | Manually add an audit note | `docs/tracking/TRACK.md` |
| `/track PRJ-101 --history` | Display audit trail for a feature | Console output |

---

## The Features Directory

Each feature lives in `docs/features/<jira-id>-<type>/`:

```
docs/features/
└── PRJ-101-story/           ← <jira-id>-<ticket-type>
    ├── context.md           ← gathered from Jira + Confluence + Bitbucket
    ├── spec.md              ← formal specification (Inputs, Outputs, ACs)
    ├── decompose.md         ← task breakdown with AC coverage matrix
    ├── plan.md              ← technical implementation plan
    └── review.md            ← 5-dimension review result
```

The global audit trail lives in:
```
docs/tracking/TRACK.md       ← every stage, every feature, auto-updated
```

---

## MCP Integrations

| Tool | Capability | Used In |
|------|-----------|---------|
| **Jira MCP** | Fetch ticket fields, ACs, linked issues | `/analysis` |
| **Confluence MCP** | Fetch linked architecture docs, business rules | `/analysis` |
| **Bitbucket MCP** | Fetch codebase patterns, PR diffs, branches | `/code`, `/review` |

If any MCP is unavailable, the agent automatically falls back to manual paste mode and tells you.

---

## Available Agents

| Agent | Role |
|-------|------|
| `analysis-agent` | Fetches and structures Jira + Confluence + Bitbucket |
| `validate-agent` | Quality-gates ACs and context completeness |
| `decompose-agent` | Ticket-type-aware task breakdown |
| `plan-agent` | Generates and validates spec.md + plan.md |
| `code-agent` | Context-rich code generation |
| `test-agent` | AC-labelled test generation with auto-run |
| `review-agent` | 5-dimension review with review.md |
| `track-agent` | Auto-appends audit trail at every stage |

---

## Available Skills

| Skill | Purpose |
|-------|---------|
| `mcp-jira` | Jira MCP fetch + structured output |
| `mcp-confluence` | Confluence MCP fetch + extraction |
| `mcp-bitbucket` | Bitbucket MCP: branches, PRs, code snippets |
| `spec-validator` | Structural + AC quality validation |
| `context-loader` | Stage-aware context bundle assembly |

---

## Useful Scripts

```bash
# Validate a spec file
node scripts/validate-spec.js docs/features/<id>/spec.md

# Check AC coverage against test files
node scripts/check-ac-coverage.js docs/features/<id>/spec.md src/test/
```

---

## Prompt Templates

Find reusable prompt templates in `prompts/`:

| File | Use For |
|------|---------|
| `prompts/05-analysis.md` | Manual Jira/Confluence analysis |
| `prompts/06-decompose.md` | Category-aware task decomposition |
| `prompts/07-plan.md` | Spec + plan generation |
| `prompts/08-review-checklist.md` | Full 5-dimension review |
| `prompts/09-confluence-push.md` | Push review.md to Confluence |
| `prompts/01-spec-to-code.md` | Code generation from spec |
| `prompts/02-test-generation.md` | Test generation |
| `prompts/03-code-review.md` | Code review vs spec |
| `prompts/04-doc-generation.md` | JavaDoc + OpenAPI + Confluence docs |

---

## Human Gates — What to Expect

At every stage, the agent pauses and waits for you:

```
⏸ HUMAN GATE — /plan
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📄 Created: docs/features/PRJ-101-story/spec.md  (validator: ✅ VALID)
📄 Created: docs/features/PRJ-101-story/plan.md

Reply "proceed" to continue, or provide feedback.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**You are always in control.** The agent suggests; you decide.

---

## Tracking Everything

Every stage is automatically logged in `docs/tracking/TRACK.md`:

```
| Stage     | Timestamp        | Actor       | Status  | Remark                            |
|-----------|------------------|-------------|---------|-----------------------------------|
| Analysis  | 2026-03-14 22:05 | agent+human | ✅ Done | Jira fetched via MCP; 4 ACs       |
| Validate  | 2026-03-14 22:18 | agent+human | ✅ Done | AC-3 reworded; Q2 deferred        |
| Plan      | 2026-03-14 22:48 | agent+human | ✅ Done | spec.md green; JWT approach       |
```

### Tracking Demos, Feedback & Requirement Changes
The standard workflow is linear, but software development is not. Use the `/track` command manually to log external events, scope changes, or demo feedback.

**CRITICAL RULE for Mid-Flight Changes**: Always state *what* it was before, *what* it changed to, and *why*. This gives agents context when they regenerate artifacts.

You can invent any stage name (like `demo`, `req-change`, or `arch-sync`):

**Example 1: Client demo feedback**
```
/track PRJ-101 demo: "Client requested email to contain user's first name instead of full name to sound more personal."
```

**Example 2: Requirement modification mid-flight**
```
/track PRJ-101 req-change: "Updated AC-2 in spec.md: Changed from full name (previous) to first-name only (new) due to PO feedback. Re-running /code."
```

These manual notes appear seamlessly in the audit trail:
```
| Demo       | 2026-03-15 10:00 | human       | 📝 Note | Client requested email to contain first name instead of full name  |
| req-change | 2026-03-15 10:30 | human       | 📝 Note | AC-2 updated: Full name -> First name only due to PO feedback      |
```

This creates a complete historical record of *why* code was rewritten or re-tested after the initial review.

To add a general manual note at any time:
```
/track PRJ-101 code: "Architect confirmed: use event sourcing"
```

---

## Tips for the Best Results

1. **Fill in context files first** — `stack.md`, `standards.md`, `architecture.md`
2. **Don't skip `/validate`** — bad ACs = bad code = expensive rework
3. **Edit `decompose.md`** before proceeding — human-approved task list = better code
4. **Read the context bundle log** at `/code` — it tells you exactly what the agent knows
5. **Use `/track` for decisions** — your future self and teammates will thank you
6. **Re-run `/review`** after every fix — don't merge with known violations

---

## Handling Mid-Flight Requirement Changes

The SDD workflow is designed to handle requirement changes at *any* stage of development. Because the agents always read the latest artifacts via the `context-loader`, you can safely loop back and re-run commands.

**Scenario**: You are in the `/code` phase, and the product owner changes a requirement.

1. **Update the Source of Truth**: Open `docs/features/<id>/context.md` (or the Jira ticket directly, then re-run `/analysis`) and update the Acceptance Criteria to reflect the new requirement.
2. **Re-Plan**: Run `/plan PRJ-101` again. The `plan-agent` will see the updated `context.md`, read the history from `TRACK.md`, and regenerate an updated `spec.md` with the new rules.
3. **Log the Change**: Run `/track PRJ-101 req-change: "Updated ACs based on PO feedback mid-sprint."`
4. **Re-Code/Test**: Run `/code PRJ-101` and `/test PRJ-101`. The agents will read the newly updated `spec.md` and modify the existing code and tests to match.

Because every stage is powered by documents, the system is fundamentally iterative. You can jump back to any previous stage, regenerate its artifact, and the downstream stages will adapt automatically.

---

## Hands-On Examples

Want to try the SDD workflow yourself? We have prepared detailed, step-by-step narrative examples showing how to use the framework in different scenarios.

👉 **[1. The Student Database (Flyway)](docs/examples/STUDENT-FLYWAY-EXAMPLE.md)** — A standard feature walkthrough.
👉 **[2. The Bug Fix Workflow](docs/examples/BUG-FIX-EXAMPLE.md)** — How the system enforces test-driven development for bugs.
👉 **[3. The Manual Copilot Workflow](docs/examples/COPILOT-MANUAL-EXAMPLE.md)** — How to use the framework manually with standard VS Code Copilot Chat (no autonomous agents required).

---

## Ticket Type Cheat Sheet

| Type | Decompose Strategy | Key Difference |
|------|-------------------|----------------|
| **Epic** | → Stories | No code generated; outputs story stubs |
| **Story** | → Layers (data, service, API, test, docs) | Standard full pipeline |
| **Task** | → current state + change + migration + tests | Focus on what changes |
| **Bug** | → fail test → root cause → fix → regression | Test written BEFORE fix |
| **Sub-task** | → dependencies + DoD | Validate already atomic |

---

*For the full original SDD walkthrough, see [WALKTHROUGH.md](WALKTHROUGH.md)*
