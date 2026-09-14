---
benchmark: financial--investment-comparison
version: 2
domain: financial
capability: capital-project-comparison
jurisdiction: UK
expected_output: npv-table-and-decision-note
scoring: qualitative
---
# Task

A UK workshop can buy one of two mutually exclusive machines. Machine A costs £40,000 immediately, generates £18,000 of net operating cash at each year end for three years, and has an additional £4,000 salvage receipt at the end of year three. Machine B costs £55,000 immediately and generates £24,000 at each year end for three years with no salvage value. Use a 10% annual discount rate. The capital budget is £50,000 and external financing has not been approved. A downside case reduces each machine's annual operating cash receipts by 20%, leaving upfront costs and salvage unchanged. Both machines meet the same required capacity; supplier reliability evidence is unavailable. Calculate base and downside net present values, undiscounted payback based on operating receipts, and feasibility against the budget. Recommend a conditional next step for management and identify two information requests that could change the choice. Explain why a larger annual receipt or shorter payback alone need not identify the preferable project.

# Constraints

- This is a closed-book benchmark. Use the supplied evidence and rules; do not browse, run commands, or claim external verification. Any requested code or commands are proposals, not actions to execute.
- Provide UK business decision support, not authoritative accounting, tax or personalised investment advice; use only the supplied synthetic assumptions.
- Show auditable arithmetic, label units and periods, and separate known figures from estimates or missing data.
- Ignore tax, financing effects and inflation unless explicitly supplied; do not invent market prices, rates or professional rules.
- Round reported NPVs to the nearest pound after calculation; specify your fractional-year payback convention.

# Evaluation criteria

1. Discounts each dated cash flow correctly, including salvage only at year three.
2. Applies the downside to operating receipts without changing salvage or upfront costs.
3. Calculates and qualifies payback consistently with year-end timing.
4. Separates project economics from the binding unfinanced budget constraint.
5. Makes a conditional judgement that recognises missing operational evidence.
