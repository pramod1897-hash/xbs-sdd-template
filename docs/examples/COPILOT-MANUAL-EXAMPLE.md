# 🤖 SDD Hands-On: Manual Copilot Workflow

Not everyone uses an autonomous agent capable of running slash commands (like `/analysis`) or reading multiple files at once. 

If your team uses **standard GitHub Copilot Chat in VS Code** (or a standard web-based LLM like ChatGPT/Claude), you can still use the exact same SDD framework! You just use the **Prompt Templates** instead of the slash commands.

Here is how you drive the SDD workflow manually. Let's work on **Ticket: PRJ-555** (Adding a logging interceptor).

---

## The Tools You Will Use
Instead of the `.agents/workflows/` directory, you will rely entirely on the `prompts/` directory:
- `prompts/05-analysis.md`
- `prompts/06-decompose.md`
- `prompts/07-plan.md`
- `prompts/01-spec-to-code.md`
- `prompts/08-review-checklist.md`

---

## Stage 1: Analysis (Creating context.md)

You open `prompts/05-analysis.md`. You copy the markdown template provided in the file and paste it into your Copilot Chat box. You fill in the blanks manually:

**Your Prompt in Copilot Chat:**
> Analyse the following Jira ticket and produce a structured context.md file.
> 
> Ticket ID: PRJ-555
> Type: Task
> 
> --- Jira Ticket Content ---
> We need a Spring `HandlerInterceptor` that logs every incoming HTTP request method and URI at INFO level.
> ...

**Copilot's Response:**
Copilot generates the markdown text for a `context.md` file. 

**Your Action:**
You physically create the file `docs/features/PRJ-555-task/context.md` in your VS Code explorer, and paste Copilot's response into it.

---

## Stage 2 & 3: Decompose and Plan

You open `prompts/06-decompose.md`. You copy the template.

Because standard Copilot can't automatically read your hard drive, you use VS Code's **Workspace Context** features (`#file`) to feed it the context.

**Your Prompt in Copilot Chat:**
> Decompose the following ticket into atomic implementation tasks.
> 
> Feature ID: PRJ-555-task
> Ticket Type: Task
> Context file: #file:docs/features/PRJ-555-task/context.md
> Stack rules: #file:.agents/context/stack.md
> 
> ... (rest of prompt from the file) ...

**Copilot's Response:**
Copilot outputs the task list matrix.

**Your Action:**
You create `decompose.md` and paste the output. You do the exact same process with `prompts/07-plan.md` to get your `spec.md` and `plan.md` files.

---

## Stage 4: Code Generation

Now you have a pristine `spec.md`, `plan.md`, and your architecture rules. You are ready to generate code. 

You open `prompts/01-spec-to-code.md`.

**Your Prompt in Copilot Chat:**
> Act as a senior software engineer. Generate code for PRJ-555-task based on these inputs:
> 
> Spec: #file:docs/features/PRJ-555-task/spec.md
> Plan: #file:docs/features/PRJ-555-task/plan.md
> Standards: #file:.agents/context/standards.md
> Architecture: #file:.agents/context/architecture.md
> 
> Please output the `LoggingInterceptor.java` and WebMvc config file.

**Copilot's Response:**
Copilot generates highly accurate, standard-compliant Java code because you fed it the exact rules (`standards.md`) and the exact contract (`spec.md`).

---

## Stage 5: Manual Tracking

Since there is no `track-agent` running in the background, you update the audit trail yourself.

You open `docs/tracking/TRACK.md` and manually add a row:

```markdown
| Code | 2026-03-15 15:00 | human (copilot) | ✅ Done | Interceptor and WebMvcConfigurer created from spec |
```

---

## Why this still works!

Even though you had to copy and paste responses and physically create the files yourself, the **quality multiplier of SDD remains identical**.

1. You forced the AI to write a strict `spec.md` contract.
2. You forced the AI to read your team's `standards.md`.
3. You separated the "thinking" (Analysis/Plan) from the "typing" (Code Generation).

By using the Prompts, any developer on any team using any basic AI chat tool can follow the SDD lifecycle.
