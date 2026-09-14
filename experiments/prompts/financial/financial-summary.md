---
benchmark: financial--financial-summary
version: 2
domain: financial
capability: executive-financial-reporting
jurisdiction: UK
expected_output: board-summary-and-actions
scoring: qualitative
---
# Task

Write a board summary of at most 250 words using this quarterly UK management packet; monetary figures are £000. Current quarter: revenue 320, gross profit 128, operating costs 118 including a separately evidenced one-off relocation cost of 20. Budget: revenue 300, gross profit 135, operating costs 110 with no relocation cost. Previous quarter: revenue 280, gross profit 126, operating costs 106. Cash fell from 52 to 22; receivables rose from 56 to 86. The only supplied bank covenant requires unrestricted quarter-end cash of at least 25; all reported cash is unrestricted. A CFO email says “the bank will probably waive any shortfall,” but there is no signed waiver. The sales forecast for next quarter is 380; 240 is contracted and 140 is an unweighted pipeline estimate. Include reported operating profit, a clearly labelled relocation-adjusted view, gross-margin movement, liquidity and covenant status, and forecast uncertainty. Give three prioritised actions. Do not imply a complete cash reconciliation can be derived from receivables alone.

# Constraints

- This is a closed-book benchmark. Use the supplied evidence and rules; do not browse, run commands, or claim external verification. Any requested code or commands are proposals, not actions to execute.
- Provide UK business decision support, not authoritative accounting, tax or personalised investment advice; use only the supplied synthetic assumptions.
- Show auditable arithmetic, label units and periods, and separate known figures from estimates or missing data.
- Ignore tax, financing effects and inflation unless explicitly supplied; do not invent market prices, rates or professional rules.
- Keep the board-facing summary within 250 words, including actions; show material calculations compactly.

# Evaluation criteria

1. Reports current, budget and previous-quarter profitability accurately.
2. Separates the one-off adjusted result from reported performance.
3. Identifies gross-margin deterioration despite revenue growth.
4. States the supplied covenant shortfall and unconfirmed waiver accurately.
5. Communicates forecast uncertainty and missing cash-bridge evidence within the limit.
