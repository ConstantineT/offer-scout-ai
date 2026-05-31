---
name: kotlin-spring-testing
description: Add or review tests for Kotlin Spring Boot services. Use when working with WebTestClient, Spring context smoke tests, service unit tests, WebClient integrations, Reactor Mono/Flux pipelines, StepVerifier, mocked collaborators, or external API smoke-test strategy.
---

# Kotlin Spring Testing

Use this skill to add focused, deterministic tests.

## Test Layers

- Test controllers, filters, and exception handlers together with `WebTestClient`.
- Test services with mocked collaborators.
- Test reactive `Mono`/`Flux` behavior with `StepVerifier`.
- Test WebClient integrations with fake `ExchangeFunction` or a mock HTTP server.
- Add one minimal `@SpringBootTest` context-load test when configuration matters.
- Keep real API/LLM tests disabled by default and separate from normal tests.

## Naming

- Use Kotlin backtick test names.
- Name tests as behavior:

```kotlin
fun `fetchPage returns fallback for timeout`() {
}
```

- Prefer: `feature returns/does/maps X when Y`.

## Style

- Use Arrange / Act / Assert structure.
- Avoid real company names, real user data, and real external APIs.
- Assert behavior, not implementation, unless the class is mostly an adapter.
- Keep assertions loose for nondeterministic AI output.
- Cover important invariants and edge cases, not every possible branch.

## Coverage

- Use JaCoCo for Kotlin coverage.
- Keep `./gradlew test` wired to generate the report and run coverage verification.
- Check the HTML report at `build/reports/jacoco/test/html/index.html`.
- Treat coverage failures as a signal to add meaningful tests first.
- Do not lower thresholds casually; prefer raising them gradually.
- Do not add empty or low-value tests only to satisfy coverage.
- Focus coverage on business logic, request boundaries, fallbacks, limits, errors, and reactive behavior.

## Useful Checks

- Success path.
- Fallback path.
- Error propagation.
- Empty/null/blank input behavior.
- Timeout behavior.
- Truncation/limits.
- Threading or scheduler behavior when it is an explicit invariant.
