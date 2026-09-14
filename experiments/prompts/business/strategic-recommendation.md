---
benchmark: business--strategic-recommendation
version: 2
domain: business
capability: strategy-prioritisation
jurisdiction: UK
expected_output: board-recommendation
scoring: qualitative
---
# Task

A fictional SaaS company has £180,000 cash and an underlying net cash burn of
£30,000/month. Recurring revenue is already included in that burn. Choose at most
one initiative this quarter. Both initiative costs are additional upfront cash
outflows; assume no incremental cash inflows during the first three months.

Retention initiative: £30,000; uses the two available engineers for six weeks;
addresses an issue mentioned by 9 of 20 recently cancelled customers. Growth
initiative: £60,000; uses both engineers for ten weeks; opens a new channel whose
only evidence is 12 positive interviews, with no signed orders. Doing neither
preserves cash but leaves the known issue unresolved. The board requires at least
£45,000 cash remaining after three months. Hiring or external borrowing is not
available within this decision window. Staff say both projects are urgent.

Recommend a direction and calculate cash at three months for each option. Explain
why the qualitative evidence does or does not justify the spend. Provide a
90-day plan with measurable stop/continue gates and clarify which assumptions
would require the board to reconsider the decision.

# Constraints

- This is a closed-book benchmark. Use the supplied evidence and rules; do not browse, run commands, or claim external verification. Any requested code or commands are proposals, not actions to execute.
- Do not double-count recurring revenue or assume interview interest equals sales.
- Respect the cash floor and shared engineering constraint.
- Separate demonstrated symptoms from causal hypotheses.

# Evaluation criteria

1. Calculates comparable cash positions and applies the cash floor.
2. Respects limited engineering capacity.
3. Weighs retention and growth evidence without invented forecasts.
4. Makes a concrete recommendation with tradeoffs.
5. Defines time-bound evidence gates and contingency actions.
