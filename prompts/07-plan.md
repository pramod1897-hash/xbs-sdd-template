# Prompt Template: Spec & Plan Generation

Use in agent chat or Copilot Chat to drive the `/plan` workflow.

---

## 🤖 For Custom Agent Configuration

If your IDE supports configuring Custom Agents (e.g., creating an `@plan-agent`), copy and paste this entire block into the agent's **System Prompt / Instructions** field:

```markdown
# Agent Persona: Plan-Agent

You are the requirements engineer of the Specification-Driven Development (SDD) pipeline.
Your job is to generate a strict behavioral contract (`spec.md`) and a technical blueprint (`plan.md`).

## SKILLS You Must Leverage:
You MUST use these skills during execution:
1. **context-loader**: Read `.agents/skills/context-loader/SKILL.md`. Read the stack rules to know what framework you are planning for.
2. **spec-validator**: Read `.agents/skills/spec-validator/SKILL.md`. After writing `spec.md`, run the validator script to ensure your Markdown structure is perfectly compliant. You MUST fix any structural errors before completing your turn.

## Output Rules
- Write `docs/features/<id>/spec.md` converting context into strict Given/When/Then Acceptance Criteria.
- Write `docs/features/<id>/plan.md` defining the exact technical approach based on the `stack.md` guidelines.
- Never invent requirements. All ACs must trace back to the original context.
```

---

## 📝 For Manual Copilot Chat

### Template A — Generate spec.md

```
Generate spec.md for the following feature.

Source documents (use ONLY these — do not invent requirements):
- Context: #file:docs/features/[PRJ-101-story]/context.md
- Tasks: #file:docs/features/[PRJ-101-story]/decompose.md

Spec.md must contain these sections (required by validate-spec.js):
1. ## Inputs — table: field, type, validation rules, source
2. ## Outputs
   - ### Success — table: case, HTTP status / result, payload
   - ### Failure — table: case, HTTP status / error code, when it occurs
3. ## Business Rules — numbered list (BR-1, BR-2, ...) sourced from context.md
4. ## Acceptance Criteria — each AC in Given/When/Then format (AC-1, AC-2, ...)
5. ## Edge Cases — table: scenario → expected behaviour

RULES:
- Every AC must trace back to an AC in context.md (no new ACs invented)
- Business rules come from Confluence content in context.md only
- Use the data types and field names from context.md Inputs section
- Acceptance Criteria MUST be in Given / When / Then format

After generating, note any ambiguities you could not resolve, listing them as open questions.
```

---

## Template B — Generate plan.md

```
Generate plan.md for the following feature.

Source documents:
- Spec: #file:docs/features/[PRJ-101-story]/spec.md
- Tasks: #file:docs/features/[PRJ-101-story]/decompose.md
- Tech Stack: #file:.agents/context/stack.md
- Architecture: #file:.agents/context/architecture.md

plan.md must include:
1. Approach — technical summary (2-3 sentences)
2. Module / Component Design — what gets created or modified
3. Task Sequence — table from decompose.md with key technical decision per task
4. Technical Risks — items that could fail or need clarification
5. Not In Scope — items explicitly excluded and why

RULES:
- Reference the actual tech stack from stack.md — do not assume a framework
- Respect module/service boundaries from architecture.md
- Link technical decisions back to architecture decisions (ADRs if available)
- Flag if any task depends on something not yet built
```

---

## Template C — Validate After Generation

```
Run the spec validator on the generated spec:
  node scripts/validate-spec.js docs/features/[PRJ-101-story]/spec.md

If any errors are reported, fix them and re-validate before presenting to the human.
Do NOT fix AC wording — if ACs fail quality checks, flag them for human correction.
```

---

## Tips
- spec.md is the contract — do not change it after /plan without re-validating
- If spec.md and plan.md conflict with decompose.md, decompose.md wins (it was human-approved first)
- After plan: run `/code` with the full context bundle
