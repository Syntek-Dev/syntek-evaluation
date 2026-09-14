---
benchmark: legal--data-protection
version: 2
domain: legal
capability: data-governance-analysis
jurisdiction: UK
expected_output: role-map-and-action-plan
scoring: qualitative
---
# Task

An England and Wales retailer proposes sending customer support conversations to a model vendor. Conversations contain names, order histories and occasional health disclosures. The synthetic project rules are: a processor uses data only on documented customer instructions; an organisation deciding a separate purpose is a controller for that purpose; production export requires a purpose, retention period, authorised recipients and documented transfer approval. The order form calls the vendor a processor and says deletion occurs after 30 days. Its separate addendum permits indefinite use of conversations to improve services for all customers and allows unspecified affiliates to access them. The vendor says names are removed, but order IDs remain and the retailer can reconnect IDs to customers. The pilot has not begun; no production data has been sent. Product proposes a one-week pilot using 500 real conversations because synthetic examples are “less realistic.” Prepare a purpose-by-purpose role map, identify contradictions and missing evidence, and propose a pilot plan with explicit go/no-go conditions. Explain what conclusions follow from the provided rules and what requires specialist legal assessment.

# Constraints

- This is a closed-book benchmark. Use the supplied evidence and rules; do not browse, run commands, or claim external verification. Any requested code or commands are proposals, not actions to execute.
- Treat all quoted provisions and interpretation rules as synthetic benchmark inputs, not statements of current UK law.
- Give preliminary analysis for an England and Wales business; distinguish contractual interpretation from questions requiring a qualified solicitor.
- Use only the supplied facts. Identify missing information instead of inventing legal authorities or commercial agreements.
- Do not cite real statutory articles or assume a transfer destination, lawful basis, consent or adequate anonymisation.

# Evaluation criteria

1. Analyses roles by actual purpose rather than accepting a contractual label.
2. Recognises re-identification potential and the sensitivity of the supplied data.
3. Reconciles retention promises with the separate reuse provision or flags the conflict.
4. Defines practical minimisation, access and deletion controls for a pilot.
5. Uses conditional decision gates and clearly identifies unresolved legal questions.
