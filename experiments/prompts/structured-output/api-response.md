---
benchmark: structured-output--api-response
version: 2
domain: structured-output
capability: api-validation-precedence
jurisdiction: UK
expected_output: json-object-only
scoring: qualitative
---
# Task

Produce the exact synthetic API response for the request below. This is a deterministic contract exercise; do not execute an API call or mutate inventory.

POST /reservations, request ID req-91, idempotency key key-8.
Body: {"items":[{"sku":"A","quantity":3},{"sku":"B","quantity":0}],"currency":"GBP"}

Contract stages run in this order and stop at the first failing stage:
1. Validate all item quantities. Each must be an integer from 1 through 20 inclusive. Emit one error for each invalid quantity, ordered by item index. A range violation uses code OUT_OF_RANGE and path items[N].quantity with zero-based N. Validation failure gives HTTP status 400 and response code VALIDATION_ERROR.
2. Check idempotency. Reusing a key with a different valid request body gives 409 and IDEMPOTENCY_CONFLICT.
3. Check stock. Insufficient stock gives 409 and INSUFFICIENT_STOCK.
4. Create the reservation and return 201 and RESERVED.

The stored key-8 belongs to a different request body. Available stock is A=2 and B=8. These downstream facts do not change stage precedence.

Every response is one JSON object with exactly request_id(string), status(integer), code(string), data(object or null), and errors(array). For any failure, data is null. At validation failure each error has exactly path(string) and code(string); no free-text messages or stock values are included. Return the one response mandated by the first failing stage.

# Constraints

- This is a closed-book benchmark. Use the supplied evidence and rules; do not browse, run commands, or claim external verification. Any requested code or commands are proposals, not actions to execute.
- Output JSON only, without an HTTP status line, Markdown fences, comments, or explanation.
- Run contract stages in the stated order and do not merge downstream failures into validation errors.
- Use exact field names, codes, paths, and JSON null values.
- Do not invent a reservation identifier, change stock, or claim that a request was sent.

# Evaluation criteria

1. Identifies the first failing contract stage.
2. Finds the invalid input with the correct indexed path.
3. Respects short-circuit precedence despite later conflicting evidence.
4. Emits the exact response shape, types, and codes.
5. Avoids side effects and unsupported success data.
