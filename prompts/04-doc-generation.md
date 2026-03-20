# Prompt Template: Documentation Generation (Javadoc + OpenAPI)

---

## 🤖 For Custom Agent Configuration

If your IDE supports configuring Custom Agents (e.g., creating a `@doc-agent`), copy and paste this entire block into the agent's **System Prompt / Instructions** field:

```markdown
# Agent Persona: Doc-Agent

You are the documentation specialist of the Specification-Driven Development (SDD) pipeline.
Your job is to generate accurate, spec-compliant documentation (Javadoc, OpenAPI, or Markdown) for the implemented code.

## SKILLS You Must Leverage:
1. **context-loader**: Read `.agents/skills/context-loader/SKILL.md` to identify the project's documentation standards from `standards.md`.

## Output Rules
- Ensure all parameters, return types, and exceptions in your documentation perfectly match the Business Rules and Outputs in the `spec.md`.
- Add explicit `@spec` or equivalent references linking back to the `spec.md`.
```

---

## 📝 For Manual Copilot Chat

### Template A: Javadoc Generation

```
Generate complete Javadoc for all public methods in #file:[implementation file] based on the spec in #file:docs/features/[feature-name]/SPEC.md.

For each method include:
- @spec reference to the spec file path
- @param — all parameters with types and descriptions from the spec Inputs table
- @return — description from spec Outputs > Success
- @throws — ALL exception types from spec Outputs > Failure, with the exact error code
- @example — a realistic usage snippet

Follow @workspace Javadoc conventions.
```

---

## Template B: OpenAPI / Swagger Annotations

```
Add Spring Web / OpenAPI annotations to #file:[Controller.java] so the automatically generated Swagger UI is accurate and human-readable.

For each endpoint, add:
- @Operation(summary = "...", description = "...")
- @ApiResponse for each HTTP status code from the spec (201, 400, 409, 404, etc.)
- @Parameter on path variables
- @RequestBody with @Schema description

Base descriptions on the spec in #file:docs/features/[feature-name]/SPEC.md.
```

---

## Template C: Confluence-Ready Documentation Page

```
Generate a Confluence-ready markdown page documenting the [module name] module.

Source files:
- Spec: #file:docs/features/[feature]/SPEC.md
- Service: #file:[AccountService.java]
- Controller: #file:[AccountController.java]

Page structure:
1. Overview (2 sentences)
2. Quick Example (curl command + response)
3. API Reference table (endpoint, method, description, request, response)
4. Business Rules (from spec)
5. Error Codes table (HTTP status, errorCode, when it occurs)
6. Related: Jira story link, test class, spec file
```
