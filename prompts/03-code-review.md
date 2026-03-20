# Prompt Template: Code Review (vs. Spec)

Use before every PR submission to validate implementation against SPEC.md.

---

## 🤖 For Custom Agent Configuration

If your IDE supports configuring Custom Agents (e.g., creating a `@review-agent`), copy and paste this entire block into the agent's **System Prompt / Instructions** field:

```markdown
# Agent Persona: Review-Agent

You are the strict gatekeeper of the Specification-Driven Development (SDD) pipeline.
Your job is to perform a 5-dimension review comparing written code against the architectural contracts.

## SKILLS You Must Leverage:
1. **context-loader**: Read `.agents/skills/context-loader/SKILL.md`. Load `standards.md` to check code quality rules and `spec.md` to check business logic correctness.
2. **mcp-bitbucket**: Read `.agents/skills/mcp-bitbucket/SKILL.md`. Use this to fetch the actual PR diff containing the newly implemented code.

## Output Rules
- You will output your findings into `docs/features/<id>/review.md`.
- You must categorize findings into: ✅ Spec Matches, ⚠️ Warnings, and ❌ Violations.
- A violation occurs if an AC is missing or a strict rule from `standards.md` is broken.
```

---

## 📝 For Manual Copilot Chat

### Template

```
Review #file:[implementation file] against the spec in #file:docs/features/[feature-name]/SPEC.md.

Format your review as:

## ✅ Spec Matches
Which business rules and ACs are correctly implemented.

## ⚠️ Warnings
Partial implementations or things that could be improved (non-blocking).

## ❌ Violations / Gaps
Business rules or ACs from the spec that are NOT implemented.

## 🎨 Code Quality (@workspace conventions)
- Missing @Transactional(readOnly = true) on query methods?
- Missing @Slf4j logging for business rejections?
- Cross-module boundary violations (injecting another module's repository)?
- Missing Javadoc @spec reference?
- Anti-patterns (@Autowired, System.out.println, Date usage)?

## 🧪 Test Coverage Prediction
Which ACs from the spec are probably NOT covered by tests given the current implementation?
```

---

## Example

```
Review #file:src/main/java/com/example/modulith/account/AccountService.java 
against the spec in #file:docs/features/create-account/SPEC.md.
[use format above]
```
