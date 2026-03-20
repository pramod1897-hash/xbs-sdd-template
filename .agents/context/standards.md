# Coding Standards & Conventions

> 📋 Fill in this file with your team's standards. Agents apply these during /code and /review.
> Be as specific as possible — vague rules produce vague code.

---

## ✅ Patterns to Follow

### Dependency Injection
<!-- e.g. Use constructor injection only. Never use field injection (@Autowired). -->

### Error Handling
<!-- e.g. Use typed exceptions. Never catch raw Exception. Each domain has its own exception types. -->

### Logging
<!-- e.g. Use @Slf4j. Log at INFO for key business decisions, WARN for handled errors, ERROR for unexpected failures. Never log passwords, tokens, or PII. -->

### Transactions
<!-- e.g. @Transactional on service methods. @Transactional(readOnly=true) for query-only methods. -->

### Validation
<!-- e.g. Validate at the API boundary using annotations. Never duplicate validation in service layer. -->

### DTOs
<!-- e.g. Request DTOs are fully validated. Response DTOs never expose internal IDs or sensitive fields. -->

### Null Safety
<!-- e.g. Use Optional<T> for nullable returns. Never return null from public methods. -->

### Configuration
<!-- e.g. No hardcoded values. All config via environment variables / config files. -->

---

## ❌ Anti-Patterns (Do NOT Generate These)

<!-- List specific things to avoid: -->
<!-- e.g. - No @Autowired field injection -->
<!-- e.g. - No System.out.println or console.log in production code -->
<!-- e.g. - No raw SQL strings in service layer -->
<!-- e.g. - No Date type — use Instant or LocalDateTime -->
<!-- e.g. - No catching Exception broadly -->
<!-- e.g. - No business logic in controllers -->

---

## Naming Conventions

| Element | Convention |
|---------|-----------|
| Classes | <!-- e.g. PascalCase, no abbreviations --> |
| Methods | <!-- e.g. camelCase, verb-first (getUser, createOrder) --> |
| Variables | <!-- e.g. camelCase, descriptive names --> |
| Constants | <!-- e.g. SCREAMING_SNAKE_CASE --> |
| Files | <!-- e.g. match class name, one class per file --> |
| Test classes | <!-- e.g. [ClassName]Test --> |
| Test methods | <!-- e.g. should[Action]When[Condition] --> |

---

## Test Standards

- Test structure: <!-- e.g. @Nested classes for happy path / error cases / edge cases -->
- Assertion library: <!-- e.g. AssertJ, Chai, pytest assert -->
- Mocking style: <!-- e.g. BDDMockito given/then, jest.fn() -->
- Every test must have: `@DisplayName("AC-N: [description]")` or equivalent
- No `Thread.sleep()` / `setTimeout()` in tests — use proper async patterns

---

## Documentation Standards

- Public API methods: <!-- e.g. Javadoc with @param, @return, @throws, @spec reference -->
- REST endpoints: <!-- e.g. OpenAPI @Operation + @ApiResponse annotations -->
- ADRs: <!-- e.g. Add to docs/decisions/ for significant technical choices -->

---

## Security Standards

- Never log: passwords, tokens, API keys, PII
- Sanitize all user inputs before use
- Use parameterized queries / ORM — no string concatenation in queries
- Secrets via environment / secret manager only — never in code or committed files

---

## Code Review Checklist (for /review phase)
<!-- Add anything your team specifically checks in PRs: -->
<!-- e.g. - [ ] No hardcoded environment values -->
<!-- e.g. - [ ] Sensitive response fields excluded -->
<!-- e.g. - [ ] Migrations are reversible -->
<!-- e.g. - [ ] Feature flags used for risky changes -->
