# 🎓 SDD Hands-On: The Student Flyway Example

Welcome to the **Specification-Driven Development (SDD)** tutorial. We are going to walk through the exact experience of building a feature using the AI agents. 

To keep things focused, we are **not** building a massive REST API. We are just going to create a Flyway database migration project for a Student Management system, setting up the initial database schema and tables.

Imagine you've just been handed **Ticket: STD-101**.

---

### Basic Setup
Before we begin, our `.agents/context/stack.md` is filled out with:
* **Language:** SQL / Java 21
* **Framework:** Spring Boot 3
* **Database:** PostgreSQL 16
* **Migration Tool:** Flyway

This completely anchors the agents. They know exactly what tools we are targeting.

---

## Stage 1: The `analysis-agent` (Gathering Context)

*You (the Human):*
> `/analysis STD-101`

*The Agent:* 
Because we don't have a real Jira instance hooked up right now, the MCP integration gracefully falls back and the agent replies:
> "I can't reach Jira. Please paste the ticket details for STD-101."

*You:*
> "We need to initialize the database for the Student Management module using Flyway. We need a `student_schema` created, and an initial `student` table that tracks their UUID, first name, last name, enrollment date, and email (must be unique). Use standard PostgreSQL types."

The agent processes this and writes `docs/features/STD-101-story/context.md`:

```markdown
# Context: STD-101 (Story)
**Priority:** High  |  **Points:** Unestimated

## Summary
Initialize the database for the Student Management module using Flyway.

## Acceptance Criteria
1. A new schema named `student_schema` must be created.
2. A new table named `student` must be created within `student_schema`.
3. The `student` table must contain columns: UUID (id), first_name, last_name, enrollment_date, and email.
4. The `email` column must enforce uniqueness.
5. All column types must use standard PostgreSQL data types.

## Open Questions
- Q1: What are the maximum length constraints for `first_name` and `last_name`?
- Q2: What is the maximum length constraint for `email`?
```

Notice how it extracted the core fields but identified the lack of specific constraints (like max name length) as open questions.

**💡 Tip:** The agent automatically pauses here at a **Human Gate**. It's giving you a chance to answer those open questions in `context.md` before moving on!

*You manually add to context.md:* "Max length for names: 100. Max length for email: 255."

---

## Stage 2: The `validate-agent` (Quality Check)

*You (the Human):*
> `/validate STD-101`

The `validate-agent` reads your updated `context.md`. It converts your raw text into testable Acceptance Criteria (ACs) and checks them for completeness.

It outputs a report stating that your requirements are clear, testable, and not duplicated. You're good to go.

*The `track-agent` quietly logs:*
> `| Validate | 14:10 | agent+human | ✅ Done | Context validated; 3 clear ACs extracted |`

---

## Stage 3: The `decompose-agent` (Breaking it down)

*You (the Human):*
> `/decompose STD-101`

The agent recognizes this is a technical Story and breaks it into atomic tasks. It generates `docs/features/STD-101-story/decompose.md` containing:

* **T-1**: Create `V1__init_student_schema.sql` (Creates `student_schema`)
* **T-2**: Create `V1.1__create_student_table.sql` (Creates table with PostgreSQL specific types and unique constraint)

**💡 Thought:** Why separate files? Flyway best practices separate schema creation from table creation. Because the agent read your `stack.md` (which specified Flyway and PostgreSQL), it applied framework-specific best practices immediately.

---

## Stage 4: The `plan-agent` (The Contract)

*You (the Human):*
> `/plan STD-101`

This is the magic moment. The agent writes `spec.md` (the strict contract) and `plan.md` (the technical blueprint). 

**The generated `spec.md` includes strict Acceptance Criteria:**
* **AC-1**: Given an empty database, when `V1` runs, then `student_schema` exists.
* **AC-2**: Given `student_schema`, when `V1.1` runs, then table `student` exists with columns `id (UUID)`, `first_name (VARCHAR 100)`, `last_name (VARCHAR 100)`, `email (VARCHAR 255 UNIQUE)`, `enrollment_date (DATE)`.

The agent automatically runs `node scripts/validate-spec.js` and reports: `✅ VALID`.

---

## ⚠️ Stage 4.5: The Mid-Flight Requirement Change

Oh no! The Product Owner rushes to your desk. *"Wait! We need to track the student's status (ACTIVE, SUSPENDED, GRADUATED). Can we add that?"*

In a traditional workflow, this causes chaos. In SDD, it's trivial.

*You:*
Open `context.md` and add the new requirement.
Then, you run a manual track command so you don't lose the history of why things changed:
> `/track STD-101 req-change: "PO requested adding student status field mid-flight. Re-running /plan."`

*You:*
> `/plan STD-101`

The agent regenerates `spec.md`. **AC-2** is automatically updated to include `status (VARCHAR 50)`. 

---

## Stage 5: The `code-agent` (Execution)

*You (the Human):*
> `/code STD-101`

The agent receives the **Context Bundle**. It reads the updated `spec.md`, the `architecture.md`, and the `standards.md`. 

It writes exactly two files to your `src/main/resources/db/migration/` directory:
1. `V1__init_student_schema.sql`
2. `V1.1__create_student_table.sql`

The SQL is beautiful. It uses PostgreSQL `UUID` types. It uses `VARCHAR(100)` exactly as specified. 

---

## Stage 6: The `test-agent` & `review-agent` (Validation)

Because we are just writing SQL scripts, traditional Java unit tests don't apply directly to the SQL, but the agent suggests a Spring Boot `@DataJpaTest` or `Testcontainers` test to verify the Flyway context boots successfully.

*You:*
> `/review STD-101`

The agent scans the generated SQL against `standards.md` to ensure you aren't doing anything banned (like creating tables in the `public` schema instead of `student_schema`). It reports: `✅ 0 Violations, 0 Warnings`.

---

## The Audit Trail (Our History)

You finish the feature. A new engineer joins the team months later and wants to know how the student table was built. They open `docs/tracking/TRACK.md` and see this exact history:

```markdown
| Stage      | Timestamp | Actor       | Status  | Remark |
|------------|-----------|-------------|---------|--------|
| Analysis   | 14:00     | agent+human | ✅ Done | Context gathered manually; 2 open questions |
| Validate   | 14:10     | agent+human | ✅ Done | Context validated; 3 clear ACs extracted |
| Decompose  | 14:12     | agent+human | ✅ Done | 2 Flyway script tasks defined |
| Plan       | 14:15     | agent+human | ✅ Done | spec.md green; initial schema planned |
| req-change | 14:20     | human       | 📝 Note | PO requested adding student status field mid-flight. Re-running /plan. |
| Plan       | 14:21     | agent+human | ✅ Done | spec.md updated with status field |
| Code       | 14:25     | agent+human | ✅ Done | V1 and V1.1 SQL scripts generated successfully |
| Review     | 14:30     | agent+human | ✅ Done | 0 Violations; ready for merge |
```

**The power of SDD:** The code matches the spec perfectly. The spec reflects the PO's exact request. And the entire history of *why* the code was written that way is cemented in the audit trail forever.
