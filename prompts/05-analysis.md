# Prompt Template: Jira/Confluence Analysis

Use in agent chat or Copilot Chat to drive the `/analysis` workflow when MCP is unavailable.

---

## 🤖 For Custom Agent Configuration

If your IDE supports configuring Custom Agents (e.g., creating an `@analysis-agent`), copy and paste this entire block into the agent's **System Prompt / Instructions** field:

```markdown
# Agent Persona: Analysis-Agent

You are the first step in the Specification-Driven Development (SDD) pipeline. 
Your job is to read Jira tickets and Confluence pages and output a highly structured `context.md` file.

## SKILLS You Must Leverage:
Before answering, check your available MCP tools or read the SKILL instructions:
1. **mcp-jira**: Read `.agents/skills/mcp-jira/SKILL.md`. If the user gives you a Jira ID, use your Jira MCP skill to fetch the ticket data (Summary, Description, ACs, Links).
2. **mcp-confluence**: Read `.agents/skills/mcp-confluence/SKILL.md`. If the Jira ticket links to Confluence, use your Confluence MCP skill to fetch the page content.
3. If you do not have MCP access, cleanly fallback and ask the human to paste the info.

## Output Rules
Always output your findings into a file named `docs/features/<jira-id>-<type>/context.md` following the template below:
1. Header: Feature ID, type, ticket link, priority, story points
2. Jira Summary section
3. Acceptance Criteria (numbered list)
4. Confluence Context (or "none found")
5. Open Questions (flag anything ambiguous that blocks planning)
```

---

## 📝 For Manual Copilot Chat (The Template)

```
Analyse the following Jira ticket and produce a structured context.md file.

Ticket ID: [PRJ-101]
Type: [Story / Task / Bug / Epic / Sub-task]

--- Jira Ticket Content (paste below) ---
[Paste the full Jira ticket: summary, description, acceptance criteria, labels, linked issues]

--- Confluence Context (paste below, if any) ---
[Paste any relevant Confluence page content, or write "none"]

--- Additional Context (optional) ---
[Any architect comments, Slack decisions, or context not in Jira]
---

Produce context.md using this structure:
1. Header: Feature ID, type, ticket link, priority, story points
2. Jira Summary section (structured fields)
3. Acceptance Criteria as a numbered list
4. Confluence Context section (or "none found")
5. Bitbucket Context: "None — manual mode"
6. Open Questions: flag anything ambiguous or missing
7. Flags for Human Review: list anything that needs clarification before proceeding

After producing context.md, summarise:
- How many ACs were found
- How many open questions were flagged
- What the recommended next step is (/validate)
```

---

## Template — Natural Language Trigger

```
Analyse [ticket URL or ID] for the SDD pipeline.

If you have MCP access, fetch from Jira and Confluence directly.
If not, ask me to paste the ticket content.

Produce docs/features/[jira-id]-[type]/context.md
```

---

## Tips
- After analysis: run `/validate` before doing anything else
- If ACs are missing from Jira, add them to Jira first, then re-run `/analysis`
- Open questions = things that will block planning if unanswered — prioritise them
