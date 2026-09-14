---
benchmark: security--api-security-review
version: 2
domain: security
capability: api-authorization-review
jurisdiction: UK
expected_output: prioritised-review-and-pseudocode
scoring: qualitative
---
# Task

Review this fictional Python API. auth_user() returns the authenticated user with id, tenant_id and role. Account rows have id, tenant_id, display_name, billing_email and role. A member may edit only display_name on their own account. A tenant administrator may edit display_name and billing_email on any account in their tenant. Role changes use a separate audited workflow and are never allowed here.

    def patch_account(account_id, body):
        user = auth_user()
        account = db.get_account(account_id)
        if not account:
            return {'error': 'not found'}, 404
        for key, value in body.items():
            setattr(account, key, value)
        db.save(account)
        return account.to_dict(), 200

The route accepts JSON objects up to 8 KiB. account.to_dict() includes an internal password_reset_token field. IDs are unguessable UUIDs, and the API uses TLS. Explain the concrete authorization, input and response risks; provide corrected framework-neutral pseudocode and a compact role/ownership test matrix. Specify a consistent policy for unknown fields and inaccessible accounts. A request containing both an allowed and a forbidden field must not partially apply.

# Constraints

- This is a closed-book benchmark. Use the supplied evidence and rules; do not browse, run commands, or claim external verification. Any requested code or commands are proposals, not actions to execute.
- Treat authentication, authorization, field validation and serialization as separate checks.
- Never allow this endpoint to change id, tenant_id, role or password_reset_token.
- Use the supplied role contract; do not invent a global administrator bypass.
- Do not rely on UUID unpredictability or TLS as object authorization.

# Evaluation criteria

1. Detects object-level and field-level authorization gaps.
2. Uses trusted tenant and ownership/role context before mutation.
3. Rejects invalid fields atomically with schema validation.
4. Returns an explicit safe response representation.
5. Tests cross-tenant, same-tenant, own-account and mixed-field cases.
