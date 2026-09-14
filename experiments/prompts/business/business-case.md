---
benchmark: business--business-case
version: 2
domain: business
capability: business-case-modelling
jurisdiction: UK
expected_output: analysis-and-table
scoring: qualitative
---
# Task

A fictional service desk proposes automating ticket triage. Implementation costs
£18,000 at month zero. From month one, software and maintenance cost £1,500 per
month. In the base case it releases 70 staff hours each month, valued internally
at £45 per hour. The team will retain all staff; there is no approved revenue
from redeploying their time. The pessimistic case releases 35 hours per month;
the optimistic case releases 95. Benefits start immediately after implementation
and remain constant for 24 months. Exclude tax, financing and discounting.

An executive says the project "pays cash back within a year" and wants immediate
approval. The team has not measured the current triage workload, and the tool
made incorrect priority assignments on 6 of 100 pilot tickets without causing
customer harm.

Build a 24-month economic case and distinguish it from the incremental cash
case. Show monthly net value, total net value and simple payback for all three
scenarios. Recommend a gated decision with measurable pilot acceptance criteria.

# Constraints

- This is a closed-book benchmark. Use the supplied evidence and rules; do not browse, run commands, or claim external verification. Any requested code or commands are proposals, not actions to execute.
- Treat released staff hours as capacity value unless a cash saving is evidenced.
- Report payback from month zero and say when it lies outside the horizon.
- Discuss pilot errors without extrapolating an established production failure rate.

# Evaluation criteria

1. Uses consistent units and includes initial and recurring costs.
2. Calculates scenario economics and payback transparently.
3. Distinguishes notional capacity benefits from realised cash savings.
4. Addresses uncertainty in baseline workload and quality.
5. Proposes a decision and measurable conditions for continuing.
