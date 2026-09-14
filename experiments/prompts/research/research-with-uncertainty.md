---
benchmark: research--research-with-uncertainty
version: 2
domain: research
capability: missing-data-and-uncertainty
jurisdiction: UK
expected_output: bounded-estimate-and-follow-up-plan
scoring: qualitative
---
# Task

A fictional warehouse is evaluating a new scanner. Synthetic S1 lists the outcomes of ten equally weighted scheduled test batches: correct classifications out of 100 items were 92, 95, 90, 94, 89, missing, 96, 91, missing, and 93. For the two missing batches, all 100 items were scanned but result logs were lost during a network outage; their correctness is unknown. S2 says the old scanner correctly classified 900 of 1,000 items in a separate test last month, with complete logs. S3 is a manager's slide: “The new scanner is 92.5% accurate, reliably exceeds the old scanner, and log loss is random.” No evidence about differing item difficulty, operator assignment or the relation between outage and errors is supplied. Calculate observed-case accuracy and worst/best bounds across all 1,000 scheduled items. Assess the slide's three claims, explain why dropping missing batches or treating them as zero answers different questions, and propose a follow-up test that separates classifier performance from logging reliability. Give a decision statement that remains valid across the identified uncertainty.

# Constraints

- This is a closed-book benchmark. Use the supplied evidence and rules; do not browse, run commands, or claim external verification. Any requested code or commands are proposals, not actions to execute.
- Use only the labelled synthetic source packet; all organisations and study details are fictional benchmark inputs.
- Cite evidence with the supplied source IDs. Do not browse, fabricate real citations or imply that missing evidence has been checked.
- Separate direct observations, calculations, interpretations and unresolved questions; avoid unsupported causal or certainty claims.
- Do not impute missing outcomes, calculate unrequested significance tests or assume missingness is random.

# Evaluation criteria

1. Uses observed and scheduled denominators correctly.
2. Computes transparent worst-case and best-case bounds for missing batches.
3. Evaluates the comparative and missingness claims against available evidence.
4. Separates classification accuracy, logging completeness and test comparability.
5. Proposes a matched reliable follow-up and a conclusion robust to uncertainty.
