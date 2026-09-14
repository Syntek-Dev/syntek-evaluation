---
benchmark: project-management--sprint-planning
version: 2
domain: project-management
capability: backlog-optimisation
jurisdiction: UK
expected_output: sprint-plan
scoring: qualitative
---
# Task

Choose a fictional two-week sprint with total capacity 18 story points, including
testing. Items are indivisible and the same point scale applies to every item.
A security patch: 5 points, mandatory, business value 4. B billing correction:
5 points, mandatory, value 6. C usage dashboard: 5 points, value 8, requires D.
D event instrumentation: 3 points, value 3. E export polish: 3 points, value 4.
F onboarding copy: 2 points, value 3. Prerequisites count against this sprint's
capacity and must complete before their dependents. No items are already done.
Maximise summed stated business value after satisfying mandatory scope; ties may
be broken by lower capacity use. Do not assume the numbers measure financial ROI.

Provide the selected sprint, point and value totals, dependency order and reasons
for deferring other items. A stakeholder argues for C+E because those have the
best visible value; evaluate that request. Finish with a sprint goal, a definition
of done and one contingency if the mandatory work turns out to be larger.

# Constraints

- This is a closed-book benchmark. Use the supplied evidence and rules; do not browse, run commands, or claim external verification. Any requested code or commands are proposals, not actions to execute.
- Respect the capacity and include hidden prerequisite cost explicitly.
- Do not split stories, drop mandatory work or increase velocity by assertion.
- Separate the mathematical selection from delivery estimate uncertainty.

# Evaluation criteria

1. Finds a feasible high-value selection under the rules.
2. Accounts for prerequisite effort and ordering.
3. Explains rejected combinations quantitatively.
4. Defines a coherent goal and meaningful done criteria.
5. Gives an honest contingency for estimate growth.
