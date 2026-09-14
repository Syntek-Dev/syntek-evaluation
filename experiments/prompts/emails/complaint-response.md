---
benchmark: emails--complaint-response
version: 2
domain: emails
capability: complaint-handling
jurisdiction: UK
expected_output: email
scoring: qualitative
---
# Task

Draft a response to customer Morgan's complaint that their support portal was
unavailable yesterday, 8 September 2026. Confirmed incident facts: impact began
09:12 BST, access restored 09:47 BST, 23 customer accounts affected. Engineers
rolled back a release at 09:40. Root cause investigation is ongoing. Monitoring
shows no further errors since 09:47, but the security review is incomplete and
there is no confirmed evidence about data exposure either way.

Morgan requests an explanation, assurance it will never happen again and a full
month's refund. The contract has a service-credit process; eligibility must be
checked by the account team. You may apologise, state known facts and commit to
an investigation update by 10 September at 16:00 BST. You cannot promise a refund,
zero future incidents or a completed root-cause report by that time.

Return a subject and email body for the support manager's approval. Balance
accountability with precision and give Morgan a clear next point of contact.

# Constraints

- This is a closed-book benchmark. Use the supplied evidence and rules; do not browse, run commands, or claim external verification. Any requested code or commands are proposals, not actions to execute.
- Body 140-190 words; use plain language and UK English.
- Label unknowns without minimising the disruption.
- Do not make a definitive data-safety claim or automatic compensation offer.

# Evaluation criteria

1. Acknowledges the complaint and impact with a direct apology.
2. States the confirmed duration and recovery facts accurately.
3. Separates investigation status from verified findings.
4. Handles refund and recurrence requests within authority.
5. Provides an exact update commitment and clear contact route.
