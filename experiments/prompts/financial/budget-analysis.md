---
benchmark: financial--budget-analysis
version: 2
domain: financial
capability: budget-variance-analysis
jurisdiction: UK
expected_output: variance-bridge-and-management-actions
scoring: qualitative
---
# Task

Explain a monthly budget miss for a UK product team. Budget: 1,000 units sold at £120 each, variable cost £50 per unit, fixed operating costs £30,000. Actual: 900 units sold for total revenue £117,000, variable costs £49,500, fixed costs £34,000. All produced units were sold; there is no inventory movement or product mix. Actual fixed costs include a one-off £3,000 equipment repair; the rest is recurring on current evidence. Build a bridge from budget operating profit to actual operating profit using this prescribed convention: volume variance uses budget unit contribution; selling-price variance uses actual units; variable-cost-rate variance uses actual units; fixed-cost variance is the direct difference. Label favourable and adverse amounts and reconcile exactly. The director says revenue is only slightly below budget, so the operating shortfall must be minor. Respond with a concise explanation, distinguish the observed shortfall from a proposed normalised view excluding the repair, and suggest two actions that follow from the separate variance drivers.

# Constraints

- This is a closed-book benchmark. Use the supplied evidence and rules; do not browse, run commands, or claim external verification. Any requested code or commands are proposals, not actions to execute.
- Provide UK business decision support, not authoritative accounting, tax or personalised investment advice; use only the supplied synthetic assumptions.
- Show auditable arithmetic, label units and periods, and separate known figures from estimates or missing data.
- Ignore tax, financing effects and inflation unless explicitly supplied; do not invent market prices, rates or professional rules.

# Evaluation criteria

1. Derives actual unit price and unit variable cost correctly.
2. Applies the prescribed variance convention consistently.
3. Reconciles the complete profit bridge without double counting.
4. Separates recurring performance from the identified one-off cost transparently.
5. Connects management actions to quantified drivers rather than revenue alone.
