# Architecture Overview

> 🏛️ Fill in this file with your system's architecture. Agents use this in /code and /review to
> respect boundaries and communication patterns. Keep it up-to-date as the system evolves.

---

## System Type
<!-- e.g. Modular Monolith / Microservices / Serverless / Monolith / Event-Driven -->

## High-Level Component Map

```
<!-- Draw or describe your modules/services here. Example:

  [Client] → [API Gateway]
                ├── account-service    → [PostgreSQL accounts_db]
                ├── notification-service → [SES / SendGrid]
                └── payment-service   → [Stripe] → [PostgreSQL payments_db]

  OR for a modular monolith:

  com.example/
  ├── account/        ← Account module (bounded context)
  ├── notification/   ← Notification module
  └── payment/        ← Payment module (not yet implemented)
-->
```

---

## Module / Service Boundaries

For each module/service, define:
- What it **owns** (data, operations)
- What it exposes publicly
- What is internal (not accessible from other modules)
- How it communicates with others

### Module: [name]
- **Owns**: <!-- entities, tables -->
- **Public API**: <!-- service interfaces, REST endpoints -->
- **Internal**: <!-- repositories, implementation details -->
- **Communicates via**: <!-- direct call, domain events, REST, gRPC -->

<!-- Repeat for each module/service -->

---

## Communication Patterns

| From | To | Pattern | Notes |
|------|----|---------|-------|
| <!-- e.g. account → notification --> | <!-- notification-service --> | <!-- domain event --> | <!-- via Spring Application Events --> |

---

## Boundary Rules (strictly enforced)

<!-- List rules that the code agent and review agent must enforce: -->
<!-- e.g. Module A must not directly import Module B's repositories -->
<!-- e.g. All cross-module calls must go through the public service interface -->
<!-- e.g. Shared DTOs live in a `shared` package — no module imports another's internal DTOs -->

### Rules
1. <!-- rule 1 -->
2. <!-- rule 2 -->
3. <!-- rule 3 -->

---

## External Dependencies & Integrations

| System | Type | Used By | Notes |
|--------|------|---------|-------|
| <!-- e.g. PostgreSQL --> | Database | <!-- account, payment --> | <!-- connection pool: HikariCP --> |
| <!-- e.g. SendGrid --> | Email | <!-- notification --> | <!-- via notification-service only --> |

---

## Non-Functional Architecture

- **Auth**: <!-- e.g. JWT Bearer tokens, validated at gateway -->
- **Rate Limiting**: <!-- e.g. per-account limits in Redis via rate-limiter module -->
- **Caching**: <!-- e.g. Redis L2 cache for product catalogue -->
- **Observability**: <!-- e.g. Micrometer → Prometheus → Grafana / OpenTelemetry -->
- **Feature Flags**: <!-- e.g. LaunchDarkly / config-based flags in feature-flag module -->

---

## Architecture Decision Records (ADRs)

<!-- Link to or summarise key decisions: -->
<!-- e.g. ADR-001: Chose modular monolith over microservices — avoid operational complexity at this scale -->
<!-- e.g. ADR-002: All async work via domain events — no direct cross-module repository injection -->

| ADR | Decision | Date | Rationale |
|-----|----------|------|-----------|
| ADR-001 | | | |
