# 🤖 Custom Agents & SKILL Conventions Guide

If your IDE or AI platform (like GitHub Copilot Enterprise, Roo Code, Cline, or Cursor) supports **Custom Agents** or **Custom Personas**, you can dramatically improve the SDD workflow by configuring dedicated agents.

Instead of typing long manual prompts, you simply configure an `@analysis-agent` or `@code-agent` once, then invoke them directly.

---

## How to Configure a Custom Agent

When creating a Custom Agent in your IDE settings, you generally need to provide three things:
1. **Agent Name**: (e.g., `analysis-agent`)
2. **Agent Description**: (e.g., "Gathers and structures Jira/Confluence context for new features.")
3. **System Prompt / Instructions**: This is the core instruction set. 

**💡 The System Prompt:** Look inside the `prompts/` directory. For every stage, we provide a `## Custom Agent System Prompt` section. You literally copy and paste that block into your IDE's agent configuration screen!

---

## Leveraging SKILLS

In the SDD framework, **Skills** are specialized tools or instructions that an Agent can use to accomplish its task. They live in the `.agents/skills/` directory.

### The SKILL Naming Convention
A skill is always structured as a directory containing a `SKILL.md` file, plus any helper scripts:

```
.agents/skills/
└── [skill-name]/              ← Lowercase, hyphenated (e.g., mcp-jira, context-loader)
    ├── SKILL.md               ← The primary instruction file for the AI
    ├── package.json           ← (Optional) If it requires dependencies
    └── script.js              ← (Optional) Executable scripts the AI can run
```

### Why `SKILL.md`?
By standardizing on `SKILL.md`, your Custom Agents (and Workflows) know exactly where to look for instructions. 

When you configure your Custom Agent, its System Prompt will explicitly say: *"Read `.agents/skills/[skill-name]/SKILL.md` to learn how to do X."*

---

## Standard SDD Custom Agents to Create

To fully power your IDE, create these Custom Agents using the System Prompts found in the `prompts/` directory:

| Agent Name | Backed By Prompt File | Skills It Leverages |
|---|---|---|
| `@analysis-agent` | `prompts/05-analysis.md` | `mcp-jira`, `mcp-confluence` |
| `@validate-agent` | `prompts/xx-validate.md` | `spec-validator` |
| `@decompose-agent`| `prompts/06-decompose.md` | `context-loader` |
| `@plan-agent` | `prompts/07-plan.md` | `spec-validator` |
| `@code-agent` | `prompts/01-spec-to-code.md` | `mcp-bitbucket` |
| `@test-agent` | `prompts/02-test-generation.md` | `none` |
| `@review-agent` | `prompts/03-code-review.md` | `mcp-bitbucket` |
| `@track-agent` | *Configured internally* | `none` |

*(Note: If you have autonomous MCP capabilities enabled in your IDE, the agent will automatically execute the MCP servers defined in the SKILL.md files!)*
