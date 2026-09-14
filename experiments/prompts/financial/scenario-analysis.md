---
benchmark: financial--scenario-analysis
version: 2
domain: financial
capability: probability-weighted-scenarios
jurisdiction: UK
expected_output: scenario-table-and-decision-memo
scoring: qualitative
---
# Task

A UK training company is considering one quarter of a new workshop programme. Use three mutually exclusive, exhaustive management scenarios, which are judgemental assumptions rather than calibrated probabilities. Base, probability 50%: sell 1,200 places at £50 each, variable cost £30 per place, fixed cost £18,000. Downside, probability 30%: sell 800 at £48, variable cost £31, fixed cost £18,000. Upside, probability 20%: sell 1,600 at £52, variable cost £32, fixed cost £20,000. Fixed costs are avoidable if the programme does not launch; there is no other profit or loss in the no-launch option. Marketing proposes reporting only the probability-weighted revenue because it looks strongest. Compute revenue, contribution and operating result in each scenario, the probability-weighted operating result and the assumed probability of a loss. Calculate break-even whole places using base price and costs. Recommend a launch condition or staged alternative, and explain what the expected result does and does not tell management about cash needs and real-world risk.

# Constraints

- This is a closed-book benchmark. Use the supplied evidence and rules; do not browse, run commands, or claim external verification. Any requested code or commands are proposals, not actions to execute.
- Provide UK business decision support, not authoritative accounting, tax or personalised investment advice; use only the supplied synthetic assumptions.
- Show auditable arithmetic, label units and periods, and separate known figures from estimates or missing data.
- Ignore tax, financing effects and inflation unless explicitly supplied; do not invent market prices, rates or professional rules.
- Use the stated scenario probabilities without implying that a profitable expected value guarantees a profitable quarter.

# Evaluation criteria

1. Calculates each scenario from its own price, volume and costs.
2. Weights operating results correctly and checks that probabilities sum to one.
3. Computes break-even volume with an appropriate whole-place rounding rule.
4. Distinguishes expected profit, loss likelihood and cash timing.
5. Proposes a decision condition grounded in downside exposure and assumption quality.
