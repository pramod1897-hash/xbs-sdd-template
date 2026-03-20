# SDD Lifecycle Audit Trail

> Auto-updated by `track-agent` at the end of each workflow stage.  
> Manual entries can be added via `/track [feature-id] [stage]: "remark"`  
> Do not edit ✅ Done rows — add a new Note row instead.

---

## How to Read This File

| Column | Meaning |
|--------|---------|
| Feature | `<jira-id>-<type>` matching the `docs/features/` directory |
| Stage | Which workflow stage completed, or an external event like `Demo` or `Req Change` |
| Timestamp | Local time when the stage was completed |
| Actor | Who did the work: `agent+human`, `mcp+human`, `human` |
| Status | ✅ Done / ⚠️ Blocked / ⏭️ Skipped / 📝 Note |
| Remark | Short, meaningful, past-tense note about what happened |

---

## PRJ-000-story — [Sample / Template Feature]

| Stage | Timestamp | Actor | Status | Remark |
|-------|-----------|-------|--------|--------|
| Analysis | YYYY-MM-DD HH:MM | agent+human | ✅ Done | Jira fetched via MCP; N ACs confirmed; Confluence arch page attached |
| Validate | YYYY-MM-DD HH:MM | agent+human | ✅ Done | AC-N reworded for testability; open question Q1 answered |
| Decompose | YYYY-MM-DD HH:MM | agent+human | ✅ Done | N tasks; [story/bug/epic] path; T-N removed as out of scope |
| Plan | YYYY-MM-DD HH:MM | agent+human | ✅ Done | spec.md validated green; key decision: [decision summary] |
| Code | YYYY-MM-DD HH:MM | agent+human | ✅ Done | N files generated; standards applied; 1 TODO flagged for follow-up |
| Test | YYYY-MM-DD HH:MM | agent+human | ✅ Done | N tests; N/N ACs covered; all passing |
| Review | YYYY-MM-DD HH:MM | agent+human | ✅ Done | N violations fixed; N warnings accepted; approved for merge |
| Demo | YYYY-MM-DD HH:MM | human | 📝 Note | Client requested email to contain user's first name, not full name |
| Req Change | YYYY-MM-DD HH:MM | human | 📝 Note | Updated AC-2 in spec to reflect first-name requirement; re-running /code |

---

<!-- New feature sections will be appended below by track-agent -->
