---
benchmark: debugging--python-stacktrace
version: 2
domain: debugging
capability: exception-root-cause
jurisdiction: UK
expected_output: diagnosis-and-code
scoring: qualitative
---
# Task

A fictional Python 3.12 importer handles supplier records. A record must have id: str and profile: object containing email: str. The supplier sometimes sends malformed records; valid records later in the same batch must still be processed. send_email is an injected function and may raise DeliveryError, which should abort the batch so the caller can retry delivery. Validation failures must be reported with the record index and id when available, without logging email addresses or whole payloads.

    def import_batch(records, send_email):
        for record in records:
            send_email(record['profile']['email'])

Traceback (most recent call last):
  File "importer.py", line 3, in import_batch
    send_email(record['profile']['email'])
KeyError: 'profile'

Captured batch:
[{"id":"c17","profile":{"email":"a@example.test"}},
 {"id":"c18"},
 {"id":"c19","profile":{"email":"b@example.test"}}]

Explain exactly what this traceback does and does not establish. Supply a small replacement that validates the specified structure, returns a validation-error summary, and honours delivery-failure behaviour. Discuss whether retrying this entire batch is automatically safe after some deliveries succeed.

# Constraints

- This is a closed-book benchmark. Use the supplied evidence and rules; do not browse, run commands, or claim external verification. Any requested code or commands are proposals, not actions to execute.
- No external libraries or tools; use structural validation rather than a complex email-address parser.
- Do not catch every exception around send_email or silently substitute a made-up email address.
- Treat None, lists, absent fields, and wrong field types as invalid structure.
- Keep contact details out of diagnostics and explain any duplicate-delivery assumption.

# Evaluation criteria

1. Locates the failing lookup using the actual traceback.
2. Separates malformed input from downstream operational failure.
3. Continues after validation failures while preserving delivery exceptions.
4. Returns useful redacted diagnostics for boundary cases.
5. Recognises partial side effects and retry/idempotency risks.
