---
benchmark: reasoning--resource-allocation
version: 2
domain: reasoning
capability: discrete-resource-optimisation
jurisdiction: UK
expected_output: allocation-and-proof
scoring: qualitative
---
# Task

A synthetic overnight compute window has exactly 10 GPU-hour tokens and 12 memory-hour tokens available. Jobs are indivisible: each job either runs once in full or does not run, and partial completion earns no value. All selected jobs consume their listed tokens from the same window; ordering does not affect feasibility. No additional time, power, or staffing constraints exist.

Job | GPU tokens | Memory tokens | Value points
A | 6 | 4 | 15
B | 4 | 8 | 12
C | 5 | 5 | 13
D | 3 | 4 | 9
E | 2 | 3 | 6

Job D is eligible only if E is also selected in the same window. E can run without D, and this dependency does not change either job's resource consumption. Every other subset condition is captured above. The objective is to maximise total value points, then minimise unused GPU tokens if several subsets tie, then choose the alphabetically earliest sorted job list if still tied.

Choose the optimal subset. Report total use and unused amount for both resources and total value. Provide an auditable optimality argument that considers feasible competing subsets or an equivalent exhaustive method. Also explain why ranking jobs by one resource-efficiency ratio cannot, by itself, prove the answer.

# Constraints

- This is a closed-book benchmark. Use the supplied evidence and rules; do not browse, run commands, or claim external verification. Any requested code or commands are proposals, not actions to execute.
- Do not exceed either budget, split jobs, repeat jobs, or ignore the dependency.
- Use exact integer arithmetic.
- Apply tie-breakers only after comparing total value.
- Make the optimality argument reproducible without relying on an unseen solver result.

# Evaluation criteria

1. Interprets both capacities and the dependency correctly.
2. Reports a feasible selected subset and accurate totals.
3. Demonstrates optimality against the meaningful alternatives.
4. Handles the specified objective and tie-break order consistently.
5. Explains the limitation of a greedy ratio for this discrete problem.
