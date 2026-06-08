# AGENTS.md

Short instructions for AI agents working in `scout-agent`.

## How To Reply

- Be concise. Prefer short answers and compact bullet lists.
- Explain only what is needed for the current task.
- If the user asks for more detail, expand then.

## Project Basics

- Kotlin / Spring Boot / WebFlux service.
- Main endpoint returns JSON offer evaluations from `evaluation`.
- Spring AI tools are in `tool/WebTool.kt`.
- Tavily/Jina web calls are in `webintegration`.

## Important Rules

- Keep controllers non-blocking by returning `Mono` when work is offloaded.
- Treat Spring AI `@Tool` calls as blocking.
- Keep the AI/tool workflow offloaded with `subscribeOn(Schedulers.boundedElastic())`.
- Keep `webintegration` reactive; `WebTool` is the blocking adapter that calls `.block()`.
- Keep `parallel-tool-calls: false` unless the tool design changes.
- Keep `spring-boot-devtools`; it supports IntelliJ rebuild/restart workflow.
- Avoid magic numbers and string literals when configuration would make the intent clearer.
- Production deployment is private Cloud Run; secrets come from Secret Manager env vars.
- Terraform infrastructure applies are manual; GitHub Actions only pushes images and updates Cloud Run revisions.
- Use `X-Correlation-Id` for request correlation; keep cid handling in the filter/MDC, not in individual log messages.
- Keep production logs concise but useful at `INFO`: request, model, tool, web search, and page-fetch milestones are enough.

## Verify Changes

Run from this directory:

Windows:

```powershell
.\gradlew.bat test
.\gradlew.bat bootJar
```

Unix:

```bash
./gradlew test
./gradlew bootJar
```

`test` also runs JaCoCo coverage report and verification.
Coverage report: `build/reports/jacoco/test/html/index.html`.

If packaging fails because of stale duplicate classes, run:

Windows:

```powershell
.\gradlew.bat clean bootJar
```

Unix:

```bash
./gradlew clean bootJar
```
