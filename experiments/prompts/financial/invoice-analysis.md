---
benchmark: financial--invoice-analysis
version: 2
domain: financial
capability: invoice-reconciliation
jurisdiction: UK
expected_output: reconciliation-table-and-payment-recommendation
scoring: qualitative
---
# Task

Review a UK supplier invoice before payment using the explicit synthetic tax treatment below. Purchase order: 100 units at £12 each; a 10% discount applies to goods only; shipping is £60 with no discount. For this exercise all discounted goods and shipping attract VAT at 20%. Supplier invoice INV-014 displays goods £1,200, shipping £60, VAT £252 and total £1,512; it omits the agreed discount. A valid credit note for £120 including VAT has already been allocated to this invoice, and a £500 bank payment has cleared against it. The accounts system also contains INV-O14, with letter O rather than zero, for the same supplier, order, date and £1,512 amount. It came from a second scan; no separate delivery is recorded, but duplication is not yet confirmed. Calculate the correct net, VAT, gross and remaining balance after the credit and payment. Explain the discrepancy, specify what should be held pending confirmation, and draft a short supplier clarification that does not accuse anyone of fraud.

# Constraints

- This is a closed-book benchmark. Use the supplied evidence and rules; do not browse, run commands, or claim external verification. Any requested code or commands are proposals, not actions to execute.
- Provide UK business decision support, not authoritative accounting, tax or personalised investment advice; use only the supplied synthetic assumptions.
- Show auditable arithmetic, label units and periods, and separate known figures from estimates or missing data.
- Ignore tax, financing effects and inflation unless explicitly supplied; do not invent market prices, rates or professional rules.
- Use only the supplied 20% treatment; do not infer real VAT eligibility, invoice validity requirements or a right to unilateral set-off.

# Evaluation criteria

1. Applies the discount to goods only and computes VAT on the correct base.
2. Reconciles gross liability, allocated credit and cleared payment once each.
3. Identifies the possible duplicate without assuming a second liability or fraud.
4. Separates arithmetic from authorisation and supplier-confirmation steps.
5. Drafts concise, evidence-based clarification and a controlled payment recommendation.
