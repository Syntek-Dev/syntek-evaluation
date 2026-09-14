---
benchmark: security--secrets-management
version: 2
domain: security
capability: secret-exposure-response
jurisdiction: UK
expected_output: incident-response-and-rotation-plan
scoring: qualitative
---
# Task

Handle a fictional credential exposure. At 10:00 UTC a developer pushed a private repository commit containing a production API token in .env. At 10:20 a CI job printed that token in a build log. At 10:40 an engineer noticed it. The token permits invoice read/write for one tenant, has no expiry, and the provider supports creating a replacement token while the old one remains valid, then revoking the old token. Three production workers read their token only at startup. CI log access is available to 25 staff and one external contractor. No evidence of misuse has yet been reviewed. Deleting the file in a new commit leaves the earlier commit accessible. The token itself is intentionally not supplied in this fixture.

Provide a time-ordered containment and recovery plan that keeps the service running where feasible. Include provider revocation, replacement distribution, worker rollout and verification, repository/history and log handling, evidence preservation, and an appropriately scoped investigation. Explain why deleting the latest .env file or rewriting Git history alone would not make the exposed token safe. Recommend three preventive controls grounded in this incident. Do not assert that an invoice data breach occurred or that a private repository made exposure harmless.

# Constraints

- This is a closed-book benchmark. Use the supplied evidence and rules; do not browse, run commands, or claim external verification. Any requested code or commands are proposals, not actions to execute.
- Do not request, reproduce or place the token in commands, tickets, reports or examples.
- Prioritise invalidating exposed authority; coordinate evidence handling without extending exposure unnecessarily.
- Avoid destructive blanket log/history deletion and coordinate any disruptive history rewrite.
- Distinguish confirmed credential exposure from unconfirmed use or data access.

# Evaluation criteria

1. Prioritises token containment and minimizes active exposure.
2. Plans replacement rollout across all startup-only consumers with verification.
3. Handles retained copies, logs and evidence without treating deletion as revocation.
4. Scopes investigation to permissions, access and the known timeline.
5. Proposes practical preventive controls and accurately states incident certainty.
