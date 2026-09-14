---
benchmark: legal--contract-review
version: 2
domain: legal
capability: contract-review
jurisdiction: UK
expected_output: risk-table-and-redlines
scoring: qualitative
---
# Task

Review a proposed software services agreement for a small England and Wales customer. Annual fees are £48,000, paid £12,000 quarterly in advance; signature and first payment are on 1 April. Main clause 8 says: “Supplier's aggregate liability is fees actually paid during the three months preceding the event.” Clause 9 says: “Customer indemnifies Supplier without limit for all claims arising from Customer's use.” Main clause 12 permits termination only after an uncured material breach and a 30-day cure period. Schedule A promises 99.9% monthly availability but says credits are the “sole remedy for any interruption, including persistent failure.” Schedule B allows Supplier to terminate for convenience on seven days' notice and retain prepaid fees. The agreement says schedules prevail over the main body, but gives no priority between schedules. The customer operates booking services and cannot replace the supplier within seven days. Deliver a prioritised review table and three short replacement clauses addressing the highest risks. Explain the April liability-cap calculation and any uncertainty about how the remedy provisions interact.

# Constraints

- This is a closed-book benchmark. Use the supplied evidence and rules; do not browse, run commands, or claim external verification. Any requested code or commands are proposals, not actions to execute.
- Treat all quoted provisions and interpretation rules as synthetic benchmark inputs, not statements of current UK law.
- Give preliminary analysis for an England and Wales business; distinguish contractual interpretation from questions requiring a qualified solicitor.
- Use only the supplied facts. Identify missing information instead of inventing legal authorities or commercial agreements.
- Do not assume an indemnity, exclusion or termination provision is enforceable merely because it appears in the agreement.

# Evaluation criteria

1. Prioritises commercially significant exposure using the stated customer circumstances.
2. Calculates the example cap from payments actually made and distinguishes it from annual contract value.
3. Explains the schedule priority rule and its limits without silently resolving every ambiguity.
4. Drafts targeted clauses that work together on remedies, liability and termination.
5. Separates evidenced interpretation, negotiation preferences and questions for legal advice.
