---
benchmark: financial--pricing-analysis
version: 2
domain: financial
capability: pricing-and-unit-economics
jurisdiction: UK
expected_output: pricing-table-and-recommendation
scoring: qualitative
---
# Task

A UK online seller currently sells 1,000 subscriptions each month at £50 each. Variable servicing cost is £25 per subscription and payment processing costs 2% of selling price. Fixed monthly operating costs are £12,000. Marketing proposes a £45 price and forecasts 1,200 monthly subscriptions. Maximum service capacity is 1,250 subscriptions per month, with no approved expansion. Assume costs and prices are net of tax, all subscriptions are paid in the month, cancellations are already reflected in stated volume, and no other costs change within capacity. Compute current and proposed unit contribution, revenue and monthly operating profit. Calculate the minimum whole subscription volume needed at £45 to preserve current profit, then compare that threshold with capacity. A manager says “20% more customers means 20% more profit”; assess the claim and propose a decision based on the supplied constraints. Include one sensitivity or data request that would materially improve the forecast, keeping guessed results clearly separate from the calculations.

# Constraints

- This is a closed-book benchmark. Use the supplied evidence and rules; do not browse, run commands, or claim external verification. Any requested code or commands are proposals, not actions to execute.
- Provide UK business decision support, not authoritative accounting, tax or personalised investment advice; use only the supplied synthetic assumptions.
- Show auditable arithmetic, label units and periods, and separate known figures from estimates or missing data.
- Ignore tax, financing effects and inflation unless explicitly supplied; do not invent market prices, rates or professional rules.
- Calculate processing fees from selling price rather than fixed cost, contribution or profit; round required volume upward.

# Evaluation criteria

1. Calculates processing fees and unit contribution for both prices.
2. Shows complete revenue and operating-profit comparisons.
3. Solves the volume threshold and rounds to a feasible whole subscription count.
4. Tests the threshold against capacity and distinguishes revenue from profit growth.
5. Gives a conditional commercial recommendation and a relevant forecast-validation step.
