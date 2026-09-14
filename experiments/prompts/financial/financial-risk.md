---
benchmark: financial--financial-risk
version: 2
domain: financial
capability: treasury-risk-analysis
jurisdiction: UK
expected_output: exposure-table-and-risk-actions
scoring: qualitative
---
# Task

A UK exporter expects one USD 50,000 customer payment in three months and must pay £35,000 of related sterling costs then. Quotes express US dollars per pound: today's planning rate is USD 1.25/GBP; downside for sterling receipts is USD 1.40/GBP; the opposite scenario is USD 1.10/GBP. A bank offers a deliverable forward at USD 1.27/GBP for the full USD 50,000, with a separate £200 fee paid from this deal's proceeds. The forward requires delivery of the dollars even if the customer pays late or defaults; no cancellation price or collateral terms are supplied. The customer represents 40% of annual revenue and has recently paid two invoices 20 days late. Management says “the forward removes all the risk.” Compute unhedged sterling receipts and contribution after the £35,000 costs in all three rate cases, plus forward receipts net of fee and contribution. Explain risk reduction and residual risks, and propose a decision-support checklist focused on cash timing, counterparty concentration and missing terms.

# Constraints

- This is a closed-book benchmark. Use the supplied evidence and rules; do not browse, run commands, or claim external verification. Any requested code or commands are proposals, not actions to execute.
- Provide UK business decision support, not authoritative accounting, tax or personalised investment advice; use only the supplied synthetic assumptions.
- Show auditable arithmetic, label units and periods, and separate known figures from estimates or missing data.
- Ignore tax, financing effects and inflation unless explicitly supplied; do not invent market prices, rates or professional rules.
- This is corporate treasury analysis, not a recommendation to trade; preserve the stated currency-quote direction and do not assign an invented default probability.

# Evaluation criteria

1. Converts dollars to pounds using the correct quote direction.
2. Calculates each contribution and treats the forward fee once.
3. Explains the trade-off between exchange-rate certainty and favourable-rate upside.
4. Identifies payment-timing, delivery-obligation and concentration risks that remain.
5. Prioritises missing contractual and liquidity information without guaranteeing protection.
