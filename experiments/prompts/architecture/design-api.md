---
benchmark: architecture--design-api
version: 2
domain: architecture
capability: asynchronous-api-design
jurisdiction: UK
expected_output: api-contract-and-failure-semantics
scoring: qualitative
---
# Task

Design a fictional REST API for customer data exports. An authenticated user requests an export for their tenant. Generation takes between 30 seconds and ten minutes and produces an object retained for 24 hours. The client may lose its connection after the server accepts a request and then retry. Repeating the same request must not create a second export when the same idempotency key is used within 24 hours. Reusing that key with different parameters must be rejected. Tenant identity comes from authentication; a user-supplied tenant_id is not authoritative. Export parameters are start_date and end_date, inclusive calendar dates, with a maximum 31-day interval.

Specify create, status, download and cancellation interactions, including concrete request/response examples, status codes, lifecycle states, error shape and key scoping. Address two concurrent create requests with the same key, a worker crash after writing the object but before recording completion, and a download request after expiration. Cancellation may race with completion; state a coherent observable policy. Explain how authorization works for status and download URLs and how the implementation can recover from partial failure without pretending that the database and object store share one transaction.

# Constraints

- This is a closed-book benchmark. Use the supplied evidence and rules; do not browse, run commands, or claim external verification. Any requested code or commands are proposals, not actions to execute.
- Use a versioned API namespace and UTC timestamps; date range inclusivity must be explicit.
- Do not place long-lived credentials in URLs or expose cross-tenant existence through errors.
- Assume PostgreSQL 16 plus an object store without distributed transactions; no product-specific guarantees.
- Specify what happens when a request fails validation before consuming its idempotency key.

# Evaluation criteria

1. Defines a usable asynchronous lifecycle and consistent response semantics.
2. Scopes and atomically enforces idempotency with payload comparison.
3. Handles worker/object-store partial failure and expiry.
4. Applies authorization to every resource and download path.
5. Resolves cancellation and validation edge cases explicitly.
