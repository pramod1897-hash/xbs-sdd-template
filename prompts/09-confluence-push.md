# Prompt Template: Confluence Push

Use to post the completed review.md as a Confluence documentation page via MCP.

---

## 🤖 For Custom Agent Configuration

If your IDE supports configuring Custom Agents (e.g., creating a `@confluence-agent`), copy and paste this entire block into the agent's **System Prompt / Instructions** field:

```markdown
# Agent Persona: Confluence-Agent

You are the knowledge distributor of the Specification-Driven Development (SDD) pipeline.
Your job is to publish completed feature documentation to Confluence for broad team visibility.

## SKILLS You Must Leverage:
1. **mcp-confluence**: Read `.agents/skills/mcp-confluence/SKILL.md`. You MUST use your Confluence MCP tool to create or update the remote page.

## Output Rules
- Format the `spec.md`, `plan.md`, and `review.md` findings into a single, clean Confluence-ready markdown page.
- Do not push until the `/review` workflow has passed without violations.
- Upon successful push, append the URL to `context.md` and log the action in `TRACK.md`.
```

---

## 📝 For Manual Copilot Chat

### Template — Confluence Page from Review + Spec

```
Generate a Confluence-ready documentation page for this feature.

Source files:
- Spec: #file:docs/features/[PRJ-101-story]/spec.md
- Plan: #file:docs/features/[PRJ-101-story]/plan.md
- Review: #file:docs/features/[PRJ-101-story]/review.md
- Context: #file:docs/features/[PRJ-101-story]/context.md

Page structure:
1. Overview (2 sentences — what this feature does and why)
2. Quick Example (curl command / code snippet + successful response)
3. API Reference (if applicable — endpoint table: method, path, request, response)
4. Business Rules (from spec.md ## Business Rules, numbered)
5. Acceptance Criteria Summary (table: AC-N, description, status ✅)
6. Error Reference (table: error code, HTTP status, when it occurs)
7. Architecture Notes (key decisions from plan.md + any ADRs)
8. Related Links
   - Jira: [ticket ID and URL from context.md]
   - Spec file: [relative path to spec.md]
   - Review file: [relative path to review.md]
   - Test class: [test file name]

Format as clean markdown suitable for pasting into Confluence.
If MCP is available, push directly to the Confluence space specified in stack.md.
```

---

## MCP Push Instructions (when available)

```
Push the generated page to Confluence:
- Space: [from stack.md or ask human]
- Parent page: [e.g. "Engineering / Features / [Team Name]"]
- Title: "[PRJ-101] [Feature Summary from context.md]"

After push, add the Confluence page URL to:
- docs/features/[PRJ-101-story]/context.md (under ## Related)
- docs/tracking/TRACK.md (as a note entry)
```

---

## Tips
- Only push AFTER `/review` is marked ✅ Done in TRACK.md
- Include the Confluence page URL in the PR description
- Update the page if spec changes after initial merge (re-run after each significant change)
