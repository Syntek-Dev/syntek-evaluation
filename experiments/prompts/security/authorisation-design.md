---
benchmark: security--authorisation-design
version: 2
domain: security
capability: policy-resolution
jurisdiction: UK
expected_output: authorization-matrix-and-pseudocode
scoring: qualitative
---
# Task

Implement the authorization policy for a fictional document service. A user has one role per tenant: viewer, editor or admin, plus an account suspended flag. Documents have tenant_id, owner_id and state (draft or published). A support operator is a separate identity and has no customer role unless explicitly granted. Policy is:
- Suspended users cannot perform any action.
- Every action requires membership of the document tenant.
- Viewers may read published documents only.
- Editors may read published documents and their own drafts, create documents, and edit/delete their own drafts.
- Admins may read any document in their tenant and edit/delete drafts, regardless of owner; no role may edit/delete published documents.
- Publishing is allowed only to an admin who is not the document owner.

Produce a concise decision function and an allow/deny matrix for: viewer reading own draft; editor reading another editor draft; editor deleting own draft; admin deleting published; admin publishing own draft; admin publishing another user draft; cross-tenant admin reading published; suspended admin reading a draft. State whether the policy specifies creating documents for admins and whether publishing an already-published document is defined. Resolve unspecified cases safely and list the policy clarifications needed.

# Constraints

- This is a closed-book benchmark. Use the supplied evidence and rules; do not browse, run commands, or claim external verification. Any requested code or commands are proposals, not actions to execute.
- Default to deny when required attributes or an action rule are absent; do not infer that admin automatically bypasses policy.
- Evaluate trusted identity/resource attributes, not caller-supplied role or tenant claims.
- Represent policy gaps explicitly while still answering every supplied case.
- Keep the decision logic independent from UI visibility and enforce it at the service boundary.

# Evaluation criteria

1. Applies tenant and suspension checks consistently before action rules.
2. Respects ownership, draft/published state and separation of duties.
3. Returns the correct decisions for all eight cases.
4. Identifies genuine unspecified behaviour without inventing permissions.
5. Provides clear auditable logic with default-deny handling.
