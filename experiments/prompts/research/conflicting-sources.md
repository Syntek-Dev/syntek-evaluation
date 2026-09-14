---
benchmark: research--conflicting-sources
version: 2
domain: research
capability: conflicting-evidence-reconciliation
jurisdiction: UK
expected_output: comparison-table-and-evidence-note
scoring: qualitative
---
# Task

A service team is choosing between document-routing systems A and B for next quarter's workload, expected to be 50% easy and 50% hard documents. Synthetic source S1 is a test log: A correctly routed 90 of 100 easy documents and 1 of 10 hard documents; B correctly routed 19 of 20 easy documents and 60 of 100 hard documents. All outcomes are present, but the two systems did not process the same individual documents. S2 is a vendor summary: “A has the higher overall success rate, so A is the more accurate choice for every workflow.” S3 is an analyst note: “B's success rate is higher within both recorded difficulty groups.” Difficulty labels were assigned by the test team; no inter-rater reliability data exists. Calculate the overall and within-group rates, then standardise both systems to the planned 50/50 mix. Reconcile S2 and S3, make a bounded recommendation, and design the smallest useful follow-up comparison. Include a clear explanation suitable for a non-statistical buyer of how differing case mix can reverse an aggregate ranking.

# Constraints

- This is a closed-book benchmark. Use the supplied evidence and rules; do not browse, run commands, or claim external verification. Any requested code or commands are proposals, not actions to execute.
- Use only the labelled synthetic source packet; all organisations and study details are fictional benchmark inputs.
- Cite evidence with the supplied source IDs. Do not browse, fabricate real citations or imply that missing evidence has been checked.
- Separate direct observations, calculations, interpretations and unresolved questions; avoid unsupported causal or certainty claims.
- Treat equal-mix standardisation as a descriptive estimate under supplied rates, not proof of future or causal performance.

# Evaluation criteria

1. Calculates overall and stratified rates with the correct denominators.
2. Uses the stated future workload weights for a comparable summary.
3. Explains how aggregate and within-group claims can differ without contradiction.
4. Assesses each source claim against the actual evidence.
5. Recommends a matched representative follow-up and identifies uncertainty limits.
