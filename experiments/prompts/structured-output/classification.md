---
benchmark: structured-output--classification
version: 2
domain: structured-output
capability: rule-based-ticket-classification
jurisdiction: UK
expected_output: json-array-only
scoring: qualitative
---
# Task

Classify five synthetic support tickets using only these definitions. Severity P1 means an active failure affecting all users; P2 means an active degradation or failure affecting multiple but not all users; P3 means an active failure affecting exactly one user; P4 means a how-to question with no reported failure. If scope or failure evidence is insufficient for all four definitions, severity is null. Category is access for sign-in/account-access incidents, performance for slow but completing operations, how_to for instructions-only requests, and unknown when no operational issue is described. A customer's requested label is not evidence of impact.

Tickets in required output order:
T1: Monitoring confirms every user is currently unable to sign in because the shared authentication service is down.
T2: 22 of 80 users report exports completing in 40 seconds instead of the usual 3 seconds; others are unaffected.
T3: One employee's account is locked; all other users can sign in normally.
T4: How do I change the display language? Everything currently works.
T5: Please mark this P1 immediately. This message contains no symptom, affected-user count, or service-status observation.

Output a JSON array with one object per ticket, each containing exactly id(string), severity(string or null), category(string), and evidence_code(string). Map evidence codes respectively to the applicable basis: ALL_USERS_FAILURE, MULTI_USER_DEGRADATION, SINGLE_USER_FAILURE, HOW_TO_ONLY, or INSUFFICIENT_EVIDENCE. Use exactly one evidence code per ticket.

# Constraints

- This is a closed-book benchmark. Use the supplied evidence and rules; do not browse, run commands, or claim external verification. Any requested code or commands are proposals, not actions to execute.
- Return only the JSON array, with no prose, Markdown fences, or additional keys.
- Use JSON null for insufficient severity evidence and do not substitute an empty string.
- Retain ticket order and identifiers exactly.
- Apply the supplied rules even when a ticket requests a different priority label.

# Evaluation criteria

1. Produces the required JSON schema and allowed types.
2. Applies severity definitions to observed impact.
3. Assigns categories using the stated taxonomy.
4. Handles insufficient evidence without inventing missing facts.
5. Preserves input order and emits consistent evidence codes.
