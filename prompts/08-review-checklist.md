# Prompt Template: Code Review Checklist

Use in agent chat or Copilot Chat to drive the `/review` workflow.

---

## 🤖 For Custom Agent Configuration

If your IDE supports configuring Custom Agents (e.g., creating a `@review-agent`), copy and paste this entire block into the agent's **System Prompt / Instructions** field:

```markdown
# Agent Persona: Review-Agent

You are the strict gatekeeper of the Specification-Driven Development (SDD) pipeline.
Your job is to perform a comprehensive 5-dimension review comparing the implementation against the architectural contracts.

## SKILLS You Must Leverage:
1. **context-loader**: Read `.agents/skills/context-loader/SKILL.md`. Load `standards.md`, `architecture.md`, `spec.md`, and `plan.md` to conduct your review.
2. **spec-validator**: Read `.agents/skills/spec-validator/SKILL.md`. Ensure the spec itself is valid before reviewing code against it.
3. **mcp-bitbucket**: Read `.agents/skills/mcp-bitbucket/SKILL.md`. Use this to inspect the actual PR diff.

## Output Rules
- Output your findings to `docs/features/<id>/review.md`.
- You must review across 5 dimensions: Spec Compliance, Architecture, Code Quality, Test Coverage, and Non-Functional rules.
- Any missed AC or broken architectural boundary is an automatic ❌ Violation.
```

---

## 📝 For Manual Copilot Chat

### Full Review Template

```
Perform a 5-dimension review of the following feature implementation against the spec.

Source documents:
- Spec: #file:docs/features/[PRJ-101-story]/spec.md
- Plan: #file:docs/features/[PRJ-101-story]/plan.md
- Context: #file:docs/features/[PRJ-101-story]/context.md
- Standards: #file:.agents/context/standards.md
- Architecture: #file:.agents/context/architecture.md

Implementation files:
- [list implemented source files]
- [list test files]

Format your review as review.md with exactly these sections:

## ✅ Spec Compliance
Table: AC | Implemented (file.method) | Tested (test name) | Status

## ⚠️ Warnings (non-blocking)
- W-N: [specific warning with file and line context]

## ❌ Violations (must fix before merge)
- X-N: [specific violation, which rule it breaks, what to change]

## 🏛️ Architecture Compliance
- Boundary violations (vs architecture.md)?
- Communication patterns followed?
- New external dependencies introduced?

## 🎨 Code Quality
- Standards compliance (vs standards.md) — call out each rule specifically
- Anti-patterns present?
- Sensitive data exposure risk?

## 🧪 Test Coverage
- AC coverage matrix: every AC → test
- Error paths tested (every error code in spec.md Outputs > Failure)?
- Edge cases from spec.md tested?

## 🔒 Non-Functional
- Security: input sanitization, token/secret handling, injection risk
- Performance: N+1 queries, unbounded fetches, missing pagination
- Observability: logging at key events, no sensitive data logged
- Config: no hardcoded values, environment-appropriate

## Summary
- Must Fix count: N
- Warnings count: M
- Overall status: APPROVED / NEEDS FIXES / BLOCKED
```

---

## Quick Review (Single File)

```
Review #file:[ImplementationFile] against #file:docs/features/[id]/spec.md

Show only: ✅ matches, ⚠️ warnings, ❌ violations
Keep it concise — this is a quick scan, not a full review.
```

---

## Architecture-Only Review

```
Check #file:[ImplementationFile] for module/service boundary violations.
Reference #file:.agents/context/architecture.md for the boundary rules.

Report: any imports or dependencies that cross defined boundaries.
```

---

## Tips
- Run this BEFORE creating a PR — catch issues while it's cheap to fix
- X-items must be resolved. W-items are technical debt — log in TRACK.md if accepted
- Re-run `/review` after fixing violations before marking the feature done
