---
description: Analyse a Jira ticket (story/task/bug/epic) using MCP or manual paste and produce context.md — the seed for the entire SDD pipeline.
---

# /analysis — Information Analysis Workflow

Triggered by:
- `/analysis PRJ-101`
- `/analysis https://company.atlassian.net/browse/PRJ-101`
- *"analyse story PRJ-101"* / *"gather info for PRJ-101"*

---

## Steps

### Step 1 — Extract Ticket ID
Parse the Jira ticket ID from the command or natural language input.
If no ID provided, ask: `Which Jira ticket would you like to analyse?`

### Step 2 — Create Feature Directory
Create directory: `docs/features/<jira-id>-<type>/`
Ticket type will be determined from Jira data in Step 3.

// turbo
### Step 3 — Invoke analysis-agent
Hand off to `analysis-agent.md` which:
- Loads context bundle (context-loader: stack, standards, architecture)
- Fetches from Jira via mcp-jira (falls back to manual paste)
- Fetches from Confluence via mcp-confluence (falls back to manual paste)
- Fetches Bitbucket branch/PR context via mcp-bitbucket
- Writes `docs/features/<jira-id>-<type>/context.md`

### Step 4 — ⏸ HUMAN GATE
```
⏸ HUMAN GATE — /analysis
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📄 Created: docs/features/PRJ-101-story/context.md

Please review:
• Are all ACs captured correctly?
• Are there open questions you can answer now?
• Add any context missing from Jira/Confluence

Reply "proceed" → /validate
Reply "edit" → make changes, then reply "proceed"
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Step 5 — Auto-Track
Run the track command to log this stage:
`/track <jira-id> analysis: "Context gathered; <N> ACs extracted"`

### Step 6 — Suggest Next Step
```
✅ /analysis complete for PRJ-101-story
Next: run /validate PRJ-101 to quality-check ACs
```
