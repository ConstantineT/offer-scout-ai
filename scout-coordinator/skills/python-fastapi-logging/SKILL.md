---
name: python-fastapi-logging
description: Apply concise Python and FastAPI logging practices for scout-coordinator. Use when adding, reviewing, or cleaning logs, correlation ids, request/task boundaries, integrations, or processing flows.
---

# Python FastAPI Logging

Use this skill to keep coordinator logs useful, quiet, and safe.

## Rules

- Use module loggers:

```python
log = logging.getLogger(__name__)
```

- Configure logging centrally in `logging_context.py`.
- Use Resend `email_id` as the correlation id.
- Set correlation id only at request/task boundaries with `correlation_id_scope(...)`.
- Do not manually append `cid=...` to every log message.
- Pass correlation downstream with `X-Correlation-Id`.
- Use parameterized messages:

```python
log.info("Fetched email %s with %s attachment(s)", email_id, count)
```

- Do not log API keys, webhook secrets, full email bodies, full attachment text, profile context, or full AI output.
- Log high-signal milestones at `INFO`.
- Log expected recoverable external failures at `warning`.
- Log unexpected handled failures with `exception`.
- Avoid duplicate logging: either log where the error is handled, or let it bubble.

## Scout-Coordinator Notes

- `/webhooks/resend` owns webhook verification and initial cid setup.
- `/tasks/process-email` restores cid from the Cloud Task payload.
- `EmailProcessor` may log processing milestones and sizes, not content.
- Integration clients should log sparingly; HTTP libraries already emit their own request logs when enabled.
