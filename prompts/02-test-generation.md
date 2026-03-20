# Prompt Template: Test Generation (JUnit 5 + MockMvc)

Use in Copilot Chat to generate unit and integration tests from a SPEC.md + implementation.

---

## 🤖 For Custom Agent Configuration

If your IDE supports configuring Custom Agents (e.g., creating a `@test-agent`), copy and paste this entire block into the agent's **System Prompt / Instructions** field:

```markdown
# Agent Persona: Test-Agent

You are the Quality Assurance engine of the Specification-Driven Development (SDD) pipeline.
Your job is to generate comprehensive, AC-labeled tests based on the formal contract (`spec.md`).

## SKILLS You Must Leverage:
1. **context-loader**: Read `.agents/skills/context-loader/SKILL.md` to identify the test runner and framework (e.g., JUnit, Jest, PyTest) specified in the project stack.

## Output Rules
- Read the generated `spec.md` and the implementation files.
- You must label EVERY test method/description with the exact Acceptance Criterion it covers (e.g., `@DisplayName("AC-1: ...")`).
- Your tests must cover 100% of the ACs, Error Cases, and Edge Cases listed in the spec.
```

---

## 📝 For Manual Copilot Chat

### Template A: Unit Tests (Service Layer)

```
Generate a JUnit 5 unit test class for #file:[path/to/AccountService.java] based on the spec in #file:docs/features/[feature-name]/SPEC.md.

Requirements (follow @workspace conventions):
- Use @ExtendWith(MockitoExtension.class)
- @Mock the repository and password encoder
- @InjectMocks the service
- Use @Nested classes to group: "happy path", "error cases", "edge cases"
- Label EVERY test with @DisplayName("AC-N: <AC description from spec>")
- Use AssertJ (assertThat) for assertions
- Use BDDMockito (given/then) for mocking

Cover:
- Every Acceptance Criterion in the spec (one test minimum per AC)
- All error scenarios (each exception type and code)
- Edge cases from the spec's Edge Cases table
```

---

## Template B: Controller Integration Tests (WebMvcTest + MockMvc)

```
Generate a @WebMvcTest integration test class for #file:[path/to/Controller.java] based on the spec in #file:docs/features/[feature-name]/SPEC.md.

Requirements (follow @workspace conventions):
- Use @WebMvcTest([ControllerClass].class)
- @Import the exception handler class
- @MockBean the service
- Use MockMvc for HTTP calls
- Use @Nested for grouping by endpoint: "POST /api/accounts", "GET /api/accounts/{id}"
- Label every test @DisplayName("AC-N: expected HTTP behaviour")
- Assert: HTTP status, JSON response body (jsonPath), headers (Location on 201)
- Assert: No password/passwordHash fields in ANY response

Cover:
- 201 Created with correct body + Location header
- 409 Conflict for duplicates
- 400 Bad Request for each validation rule
- 404 Not Found
```

---

## Tips

- Run tests immediately after generation: `mvn test -Dtest=AccountServiceTest`
- If a test fails — tell Copilot: *"Test AC-2 is failing because the mock isn't set up correctly. Fix the test setup."*
- For parameterized tests on validation rules: *"Convert the email validation tests to use @ParameterizedTest with @ValueSource for multiple invalid email formats"*
