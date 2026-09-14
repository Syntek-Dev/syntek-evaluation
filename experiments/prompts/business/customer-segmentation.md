---
benchmark: business--customer-segmentation
version: 2
domain: business
capability: segment-prioritisation
jurisdiction: UK
expected_output: analysis-and-ranking
scoring: qualitative
---
# Task

A fictional managed service has three segments. Figures are per active customer
per month; support labour is not yet included in gross contribution.

Solo: 60 customers, revenue £100, direct non-support cost £30, support 0.5 hours.
Agency: 25 customers, revenue £400, direct non-support cost £100, support 3 hours.
Regulated: 10 customers, revenue £900, direct non-support cost £250, support 10 hours.
Value support at £40/hour. Next quarter, expected demand is at most 20 new Solo,
eight new Agency and five new Regulated customers. The existing business already
uses its normal support team. Only 30 additional support hours per month are
available for the new customers. Onboarding cost and churn by segment are unknown.

Compare present segment economics and choose the mix of new customers that
maximises additional monthly contribution after support within the demand and
capacity limits. Customers are indivisible. Explain how the recommendation might
change if the missing evidence is adverse and propose a validation experiment.

# Constraints

- This is a closed-book benchmark. Use the supplied evidence and rules; do not browse, run commands, or claim external verification. Any requested code or commands are proposals, not actions to execute.
- Show per-customer and segment totals; do not count existing support twice.
- Use whole customer counts and account for unused capacity.
- Treat segment labels as business needs, not proxies for personal characteristics.

# Evaluation criteria

1. Computes contribution after support consistently.
2. Distinguishes total value from value per scarce support hour.
3. Provides a feasible, justified acquisition mix.
4. Recognises missing onboarding and retention evidence.
5. Proposes a measurable experiment without unsupported segment generalisations.
