# Prompt Template: Spec → Java/Spring Implementation

Use in Copilot Chat when you have a completed SPEC.md and want to generate a Spring Boot implementation.

---

## 🤖 For Custom Agent Configuration

If your IDE supports configuring Custom Agents (e.g., creating an `@code-agent`), copy and paste this entire block into the agent's **System Prompt / Instructions** field:

```markdown
# Agent Persona: Code-Agent

You are the implementation engine of the Specification-Driven Development (SDD) pipeline. 
Your job is to read architectural contracts and write production-grade code that perfectly satisfies them.

## SKILLS You Must Leverage:
Before generating a single line of code, you MUST use the following skills to gather your context:
1. **mcp-bitbucket**: Read `.agents/skills/mcp-bitbucket/SKILL.md`. Use this skill to fetch 1 existing Controller and 1 existing Service from the codebase to use as a style map. You must match the existing codebase style.
2. **context-loader**: Read `.agents/skills/context-loader/SKILL.md`. You must read `stack.md` (for framework rules), `standards.md` (for compliance), and `architecture.md` (for boundaries).

## Output Rules
- You will be provided with a `spec.md` and a `plan.md`. 
- Generate code task-by-task from the `plan.md`.
- Ensure EVERY Acceptance Criterion in the `spec.md` is handled. If the AC dictates an exception should be thrown, throw it.
- After writing the code, summarize exactly which ACs were satisfied in which files.
```

---

## 📝 For Manual Copilot Chat (The Template)

```
Using the spec in #file:docs/features/[feature-name]/SPEC.md, generate the Java implementation for the [feature name] feature in our Spring Modulith project.

Context from @workspace:
- Follow Spring Modulith module boundary rules (Repository = package-private, Service = public)
- Use our established patterns: @Transactional service, @RequiredArgsConstructor, @Slf4j
- Handle all business rules from the spec with appropriate typed exceptions
- Use Jakarta Bean Validation annotations on DTO fields
- Add @spec Javadoc reference linking to the spec file

Generate in this order:
1. Request DTO (AccountRequest.java style) with Bean Validation
2. Service method implementing all business rules from the spec
3. Controller endpoint (thin adapter, delegates to Service)
4. Exception classes if new error types are needed

For each generated class, briefly explain:
- Which business rules or ACs it implements
- Any assumptions made where the spec was ambiguous
```

---

## Example (Filled In)

```
Using the spec in #file:docs/features/create-account/SPEC.md, generate the Java implementation for the Create Account feature.

Context from @workspace:
- Follow Spring Modulith module boundary rules
- Use our established patterns: @Transactional service, @RequiredArgsConstructor, @Slf4j
- Handle all business rules with AccountAlreadyExistsException etc.
- Use Jakarta Bean Validation on AccountRequest
- Add @spec Javadoc reference

Generate: AccountRequest.java, AccountService.createAccount(), AccountController, exceptions.
```

---

## Follow-Up Prompts

```
# Fix a missing business rule
"The implementation is missing Business Rule 3 from the spec (email trim before storage). 
Please update AccountService.createAccount() to handle this."

# Add missing exception handling
"Add handling for the SERVICE_UNAVAILABLE case from the spec — wrap database exceptions 
in a typed AccountServiceException with code SERVICE_UNAVAILABLE."

# Check AC coverage
"Review #file:AccountService.java against #file:docs/features/create-account/SPEC.md.
List which ACs are implemented and which are missing."
```
