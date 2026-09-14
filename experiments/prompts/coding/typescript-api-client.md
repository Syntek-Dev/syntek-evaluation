---
benchmark: coding--typescript-api-client
version: 2
domain: coding
capability: robust-api-client
jurisdiction: UK
expected_output: analysis-and-code
scoring: qualitative
---
# Task

A fictional browser application uses TypeScript 5.4 with the DOM fetch API. GET /v1/jobs/{id} returns 200 JSON {"id": string, "state": "queued" | "done" | "failed"}; a 404 means absent. Other statuses are errors and might contain HTML, invalid JSON, or a JSON object with message: string. The endpoint is read-only. Implement getJob(id, signal?) returning Promise<Job | null> with runtime validation. Callers need errors that distinguish HTTP status failures, malformed success responses, and transport failures. An aborted request must remain distinguishable as cancellation. Include three concise usage/test examples.

For this fixture, retries are optional but, if included, allow at most one retry and only for a network failure or HTTP 503. A retry must honour the same abort signal. IDs are opaque strings: an id containing '/' or '?' is one path segment. There is no authentication work to add. Explain how your design avoids treating a TypeScript assertion as proof of the server response shape.

# Constraints

- This is a closed-book benchmark. Use the supplied evidence and rules; do not browse, run commands, or claim external verification. Any requested code or commands are proposals, not actions to execute.
- Do not use third-party packages or claim execution against a live endpoint.
- Do not retry 404, arbitrary 4xx responses, schema failures, or cancellation.
- Never expose an entire HTML error response to users; bound any diagnostic text.
- Keep the base URL fixed as https://api.example.test.

# Evaluation criteria

1. Encodes the opaque ID correctly and respects the endpoint result contract.
2. Validates all required response fields and enum values at runtime.
3. Separates HTTP, payload, transport, and cancellation failures.
4. Handles non-JSON error bodies without losing status information.
5. Provides clear, type-safe code and meaningful edge-case examples.
