---
benchmark: financial--cashflow-analysis
version: 2
domain: financial
capability: cashflow-and-liquidity-planning
jurisdiction: UK
expected_output: cashflow-table-and-liquidity-plan
scoring: qualitative
---
# Task

Build a January–March cash forecast for a UK business, using £000. Opening January cash is 25. January receipts are 30; payments are payroll 22, rent 5, suppliers 18. February receipts are 55; payments are payroll 22, rent 5, suppliers 12, VAT 9. March receipts are 35; payments are payroll 22, rent 5, suppliers 20, loan repayment 8. All March payments occur on 1 March and all March receipts arrive on 25 March. Exact timing in January and February is unavailable. Management requires a minimum cash buffer of 10. An undrawn facility of 15 is confirmed available throughout the forecast; ignore interest and fees. The director says the facility must be adequate because March month-end cash is only slightly negative. Produce monthly closing balances before financing, the known March cash trough, and funding required both for the month-end buffer and for the March trough buffer. State the additional requirement beyond the confirmed facility, distinguish forecast solvency from timing risk, and propose practical actions with decision deadlines.

# Constraints

- This is a closed-book benchmark. Use the supplied evidence and rules; do not browse, run commands, or claim external verification. Any requested code or commands are proposals, not actions to execute.
- Provide UK business decision support, not authoritative accounting, tax or personalised investment advice; use only the supplied synthetic assumptions.
- Show auditable arithmetic, label units and periods, and separate known figures from estimates or missing data.
- Ignore tax, financing effects and inflation unless explicitly supplied; do not invent market prices, rates or professional rules.
- Do not infer January or February daily lows from monthly totals, or assume customers or suppliers will accept revised timing.

# Evaluation criteria

1. Calculates each monthly balance using the previous closing balance.
2. Uses the specified March payment and receipt dates to identify the cash trough.
3. Includes the required buffer in funding needs and treats the facility as financing.
4. Distinguishes total liquidity required from the additional uncommitted amount.
5. Proposes timely conditional actions and highlights unknown earlier intra-month timing.
