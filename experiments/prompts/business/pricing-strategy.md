---
benchmark: business--pricing-strategy
version: 2
domain: business
capability: pricing-experiment
jurisdiction: UK
expected_output: pricing-proposal
scoring: qualitative
---
# Task

A fictional SaaS team is considering a price change for new customers only.
Existing customers keep their current contracts. Three mutually exclusive test
arms each receive 1,000 comparable qualified visitors over the same period.
Arm A charges £80/month and converts 40 visitors; B charges £100 and converts
36; C charges £130 and converts 25. All converted accounts completed one billed
month with no refunds. Variable hosting costs £15 per active account per month;
support costs £20 per support hour. Observed first-month mean support demand is
0.5 hours per account in A, 0.75 in B and 1.5 in C. Ignore other costs for the
comparison. No retention, acquisition cost or uncertainty intervals are available.

The founder wants the highest price because it "must produce the best margin".
Recommend the next pricing step. Show conversion, per-account contribution,
total first-month contribution and contribution per visitor. Explain how a
follow-up experiment should resolve uncertainty before applying a lasting policy.

# Constraints

- This is a closed-book benchmark. Use the supplied evidence and rules; do not browse, run commands, or claim external verification. Any requested code or commands are proposals, not actions to execute.
- Do not extrapolate lifetime value from one billed month.
- Use comparable visitor denominators and include support costs.
- Do not claim statistical significance without an appropriate analysis.

# Evaluation criteria

1. Calculates all requested metrics with consistent denominators.
2. Separates unit economics from cohort-level contribution.
3. Tests the founder claim against the evidence.
4. Addresses retention and sampling uncertainty.
5. Designs an ethical, measurable follow-up pricing test.
