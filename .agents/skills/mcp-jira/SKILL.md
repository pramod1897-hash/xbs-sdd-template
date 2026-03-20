---
name: mcp-jira
description: Fetches Jira ticket details (story, task, bug, epic) via MCP server and structures them into the SDD context format. Falls back to guided manual paste when MCP is unavailable.
---

# MCP Jira Skill

## Purpose
Connect to a live Jira MCP server and extract all fields required for the SDD analysis phase. If the MCP server is unavailable, guide the human through a structured manual paste.

---

## Mode Detection

Before fetching, check if the Jira MCP server is reachable:
- **MCP Available** → Use MCP tools to fetch ticket data
- **MCP Unavailable** → Activate Manual Fallback (see below)

Always inform the human which mode is active:
```
🔌 Jira MCP: CONNECTED — fetching PRJ-101 automatically
```
or
```
⚠️ Jira MCP: UNAVAILABLE — switching to manual mode
```

---

## MCP Fetch — Fields to Extract

When connected, extract and structure the following fields:

| Field | Jira API Path | SDD Usage |
|---|---|---|
| Ticket ID | `issue.key` | File naming (`PRJ-101-story/`) |
| Type | `issue.fields.issuetype.name` | Decomposition strategy |
| Summary | `issue.fields.summary` | Feature title |
| Description | `issue.fields.description` | Business context |
| Acceptance Criteria | `issue.fields.description` (AC section) | Spec AC table |
| Story Points | `issue.fields.story_points` | Complexity indicator |
| Priority | `issue.fields.priority.name` | Review risk level |
| Labels | `issue.fields.labels` | Domain tagging |
| Epic Link | `issue.fields.epic_link` | Parent context |
| Sprint | `issue.fields.sprint.name` | Delivery context |
| Assignee | `issue.fields.assignee.displayName` | Actor in TRACK.md |
| Linked Issues | `issue.fields.issuelinks` | Dependency mapping |
| Confluence Links | `issue.fields.remotelinks` | Hand off to mcp-confluence |
| Attachments | `issue.fields.attachment` | Supporting diagrams/docs |
| Comments | `issue.fields.comment.comments` (latest 3) | Decision context |

---

## Output Format

Produce a structured section for `context.md`:

```markdown
## 📋 Jira Ticket

- **ID**: PRJ-101
- **Type**: Story
- **Summary**: As a user, I want to reset my password via email
- **Priority**: High | **Points**: 5
- **Epic**: PRJ-90 — User Authentication Epic
- **Sprint**: Sprint 12 | **Assignee**: Jane Dev
- **Labels**: `auth`, `security`, `email`

### Description
[Full description from Jira]

### Acceptance Criteria (Raw from Jira)
1. AC-1: User receives reset email within 30s
2. AC-2: Link expires after 1 hour
3. ...

### Linked Issues
- Blocks: PRJ-102 (Enable MFA)
- Relates to: PRJ-55 (Email service)

### Key Comments
> [Date] John Arch: "Use existing email-service module, do not create new one"
```

---

## Manual Fallback

When MCP is unavailable, prompt the human:

```
⏸ MANUAL MODE: Please paste the following from your Jira ticket:

1. Ticket ID (e.g. PRJ-101):
2. Ticket Type (Story/Task/Bug/Epic/Sub-task):
3. Summary (1 line title):
4. Description (full text):
5. Acceptance Criteria (numbered list):
6. Story Points:
7. Labels:
8. Any linked tickets or decisions from comments:

✅ Once pasted, I will structure this into context.md
```

---

## Validation After Fetch

After fetching (or paste), verify:
- [ ] Ticket ID is present
- [ ] Ticket type is identified (required for decompose strategy)
- [ ] At least 1 Acceptance Criterion exists
- [ ] Summary is non-empty

If any check fails, flag to human before proceeding.
