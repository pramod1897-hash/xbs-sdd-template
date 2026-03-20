---
name: mcp-confluence
description: Fetches linked Confluence documentation pages via MCP server and extracts relevant sections for the SDD context. Falls back to guided manual paste when MCP is unavailable.
---

# MCP Confluence Skill

## Purpose
Extract technical context, architecture decisions, API contracts, and business rules from Confluence pages that are linked from a Jira ticket or explicitly provided by the human. This enriches the SDD `context.md` well beyond what Jira alone provides.

---

## Mode Detection

Check if the Confluence MCP server is reachable:
- **MCP Available** → Fetch pages using Confluence REST API via MCP
- **MCP Unavailable** → Activate Manual Fallback

Always report mode:
```
🔌 Confluence MCP: CONNECTED — fetching linked pages
```
or
```
⚠️ Confluence MCP: UNAVAILABLE — switching to manual mode
```

---

## MCP Fetch — What to Extract

### Step 1 — Identify Pages to Fetch
Sources (in priority order):
1. Remote links from the Jira ticket (via mcp-jira output)
2. URLs explicitly provided by the human
3. Space + label search: search the Confluence space for pages tagged with the story's labels

### Step 2 — For Each Page, Extract

| Section | What to Look For |
|---|---|
| **Overview / Purpose** | What this feature/service does |
| **Architecture Decisions** | ADRs, design choices, rationale |
| **API Contracts** | Endpoint definitions, request/response schemas |
| **Business Rules** | Domain rules, constraints |
| **Data Model** | Entity relationships, field definitions |
| **Non-Functional Requirements** | SLAs, security constraints, performance targets |
| **Open Questions / Risks** | Unresolved items that affect implementation |
| **Related Pages** | Links to parent/child architecture docs |

---

## Output Format

Append a structured section to `context.md`:

```markdown
## 📄 Confluence Context

### Page: Authentication Architecture (v3)
**URL**: https://company.atlassian.net/wiki/spaces/ENG/pages/12345
**Last Updated**: 2026-02-10 | **Owner**: Platform Team

#### Key Architecture Decisions
- Password reset uses a stateless signed JWT token (not a DB-stored OTP)
- Token signed with RS256; private key in Vault
- Use existing `notification-service` — do not call email provider directly

#### Business Rules Relevant to This Story
- BR-1: Reset tokens are single-use; invalidated on first click
- BR-2: Max 3 reset requests per hour per account (rate limiting)
- BR-3: Audit log entry required for every reset attempt

#### Non-Functional Requirements
- Reset email delivery < 30s (p99)
- Token validation endpoint: < 50ms p99

#### Open Questions
- ❓ Should reset for OAuth-linked accounts be blocked or redirect to IdP?
```

---

## Manual Fallback

When MCP is unavailable:

```
⏸ MANUAL MODE: Please provide the Confluence context by either:

Option A — Paste the relevant sections from Confluence:
  [Paste text here]

Option B — Provide the Confluence page URL(s):
  [URL 1]:
  [URL 2]:
  (I will note them as references in context.md — you'll need to manually extract content)

✅ I will structure whatever you provide into the Confluence section of context.md
```

---

## Validation After Fetch

After fetching:
- [ ] At least one architecture decision is captured (if page exists)
- [ ] Any non-functional requirements are noted
- [ ] Open questions are flagged for human review before Validate phase

If no Confluence pages are found/linked, note this in `context.md` and proceed:
```markdown
> ⚠️ No Confluence pages linked. Context is based on Jira ticket only. 
> Human should add additional context to context.md before proceeding to /validate.
```
