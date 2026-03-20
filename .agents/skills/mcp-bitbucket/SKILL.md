---
name: mcp-bitbucket
description: Fetches relevant codebase snippets, branches, open PRs, and recent commit context via Bitbucket MCP server. Used primarily in the /code and /review phases to maintain consistency with existing patterns. Falls back to manual guidance when MCP is unavailable.
---

# MCP Bitbucket Skill

## Purpose
Ground code generation and review in **real codebase evidence** — not generic patterns. The code agent uses this skill to pull existing implementation patterns from the repository so generated code is consistent with the team's actual style.

Key uses:
- `/code` phase: fetch existing similar modules as style reference
- `/review` phase: compare PR diff against spec
- `/analysis` phase: find related existing code/branches for a ticket

---

## Mode Detection

Check if Bitbucket MCP server is reachable:
- **MCP Available** → Fetch via Bitbucket REST API
- **MCP Unavailable** → Fall back to filesystem search + manual guidance

Always report mode:
```
🔌 Bitbucket MCP: CONNECTED — fetching codebase context
```
or
```
⚠️ Bitbucket MCP: UNAVAILABLE — using local filesystem search
```

---

## Use Case A — `/analysis` Phase: Related Branches & PRs

When a Jira ticket ID is known, search for:

| What | How |
|---|---|
| Feature branches | Branches containing the Jira ID (e.g. `feature/PRJ-101-*`) |
| Open PRs | PRs with title/description mentioning the Jira ID |
| Recent commits | Commits mentioning the Jira ID in message |

Output in `context.md`:
```markdown
## 🔀 Bitbucket Context

### Related Branches
- `feature/PRJ-101-password-reset` — created by Jane Dev, 2026-03-10, 3 commits ahead of main

### Open PRs
- PR #456: "PRJ-101 Add password reset flow" — OPEN, 2 reviewers pending

### Related Commits (last 5 mentioning PRJ-101)
- abc123: "Add password reset token model" — Jane Dev, 2026-03-12
```

---

## Use Case B — `/code` Phase: Existing Pattern Fetch

Fetch existing implementation files that are **structurally similar** to what will be generated, so the code agent can match patterns.

### Strategy (in order)
1. Check `.agents/context/architecture.md` for module/service listing
2. Fetch 1-2 existing service files from the same layer as a style reference
3. Fetch 1 existing test file as test pattern reference
4. Note which patterns to follow vs avoid (cross-reference with `standards.md`)

Output snippet injected into code agent context:
```markdown
## 📂 Codebase Style Reference

### Existing Service Pattern (from NotificationService)
```[language from stack.md]
// Example: constructor pattern, error handling, logging conventions
// [fetched snippet here]
```

### Existing Test Pattern (from AccountServiceTest)
```[language from stack.md]
// [fetched snippet here]
```

> ✅ Follow these patterns. Do NOT deviate unless spec.md requires it.
```

---

## Use Case C — `/review` Phase: PR Diff Review

Fetch the PR diff for the Jira ticket's branch and pass to the review agent for spec-vs-code comparison.

```markdown
## 🔍 PR Diff Summary

### PR #456: PRJ-101 password reset
- Files changed: 6
- Additions: 142, Deletions: 8
- [diff content passed to review-agent]
```

---

## Filesystem Fallback (No MCP)

When MCP is unavailable, use local filesystem tools to find similar files:

```
⏸ FILESYSTEM MODE: Searching local codebase for similar patterns...
  → Scanning src/ for existing service/controller/test patterns
  → Found: [list of relevant local files]
  → Using these as style reference (Bitbucket MCP unavailable)
```

---

## Validation

After fetching:
- [ ] At least one style reference file found (for `/code` phase)
- [ ] Branch/PR status noted for in-progress tickets
- [ ] No conflicting open PRs on same module flagged to human
