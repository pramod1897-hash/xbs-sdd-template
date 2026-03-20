---
description: Generates comprehensive, AC-labelled tests from spec.md ACs, runs them, and surfaces failures with targeted fix guidance.
---

# /test — Test Generation Workflow

Triggered by:
- `/test PRJ-101`
- *"generate tests for PRJ-101"* / *"write tests for PRJ-101"* / *"test PRJ-101"*

---

## Pre-condition Check
If `docs/features/<id>/spec.md` does not exist:
```
❌ spec.md not found. Run /plan PRJ-101 and /code PRJ-101 first.
```

---

## Steps

### Step 1 — Load Context Bundle
Invoke context-loader for stage `/test`: reads stack, standards, spec.md, plan.md.
Identify test framework and runner command from stack.md.

### Step 2 — Build AC-to-Test Mapping
Display planned test coverage before generating:
```
📋 Test plan for PRJ-101-story:
  AC-1 → unit: shouldSendResetEmail | integration: POST_200_initiates
  AC-2 → unit: shouldReturn404ForUnknownEmail | integration: POST_404_notFound
  AC-3 → unit: shouldReturn429WhenRateLimited | integration: POST_429_rateLimit
  AC-4 → unit: shouldInvalidateUsedToken
  Edge → unit: shouldBeCaseInsensitiveForEmail
```

### Step 3 — Invoke test-agent
Hand off to `test-agent.md` which:
- Generates unit tests from spec.md + generated service/logic files
- Generates integration/API tests from spec.md Outputs table
- Labels every test with its AC
- Follows test structure from standards.md

### Step 4 — Run Tests
Execute: `[test runner command from stack.md]`

Display results:
```
Tests run: 12 | Passed: 12 | Failed: 0 ✅
```
If failures:
```
❌ FAILED: [test name]
   Reason: [specific reason]
   Fix: [targeted fix instruction]
```
Apply fixes and re-run until green.

### Step 5 — AC Coverage Report
Display the AC coverage matrix (from test-agent):
```
AC Coverage: 4/4 ✅
Error paths: 3/3 ✅
Edge cases: 1/1 ✅
```

### Step 6 — ⏸ HUMAN GATE
```
⏸ HUMAN GATE — /test
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
All tests: ✅ 12/12 passing
AC Coverage: 4/4

Optional review:
• Add edge cases not covered?
• Verify @DisplayName labels are readable?

Reply "proceed" → /review
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Step 7 — Auto-Track
Run the track command to log this stage:
`/track <jira-id> test: "<M>/<N> tests passing; <X>/<Y> ACs covered"`

### Step 8 — Suggest Next Step
```
✅ /test complete — 12/12 passing, 4/4 ACs covered
Next: run /review PRJ-101 for the final quality gate
```
