---
benchmark: financial--financial-analysis
version: 2
domain: financial
capability: financial-statement-analysis
jurisdiction: UK
expected_output: profit-and-cash-reconciliation
scoring: qualitative
---
# Task

Analyse one month for a small UK distributor; all figures are in £000 and tax is excluded. Revenue is 200, cost of goods sold 112, operating expenses excluding depreciation 56, depreciation 8 and interest expense 4. Cash collected from customers is 180; supplier payments are 115; operating-expense cash payments are 54; interest paid is 4. Opening/closing balances are receivables 30/50, inventory 25/40, trade payables 20/32 and operating-expense accruals 3/5. Cash starts at 18. A machine purchase consumes 20 cash and a new loan provides 15 cash; there are no other movements. The owner says “profit means we generated 20 cash, so the cash account must rise by 20.” Prepare the income result through profit before tax, direct and indirect operating-cash reconciliations, and a closing-cash bridge. Calculate gross and operating margins, identify the main cash-conversion pressures and propose two follow-up checks. Distinguish working-capital timing from evidence of bad debts or obsolete inventory, which is not supplied.

# Constraints

- This is a closed-book benchmark. Use the supplied evidence and rules; do not browse, run commands, or claim external verification. Any requested code or commands are proposals, not actions to execute.
- Provide UK business decision support, not authoritative accounting, tax or personalised investment advice; use only the supplied synthetic assumptions.
- Show auditable arithmetic, label units and periods, and separate known figures from estimates or missing data.
- Ignore tax, financing effects and inflation unless explicitly supplied; do not invent market prices, rates or professional rules.

# Evaluation criteria

1. Calculates profit and margins with depreciation and interest in the correct places.
2. Reconciles operating cash by both direct and indirect methods.
3. Uses working-capital changes with correct signs and avoids double counting.
4. Bridges opening to closing cash including investing and financing movements.
5. Explains the practical cash pressure without asserting unsupported asset impairment.
