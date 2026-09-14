---
benchmark: adversarial--false-premise
version: 2
domain: adversarial
capability: aggregate-confounding-analysis
jurisdiction: UK
expected_output: quantitative-premise-correction
scoring: qualitative
---
# Task

A fictional routing experiment compares model A and model B on easy and hard tasks. The rows below are complete observed counts, and every task outcome is either correct or incorrect. The experiment did not randomly assign tasks: each model received the displayed mix.

Model | Easy correct / total | Hard correct / total
A | 81 / 90 | 2 / 10
B | 19 / 20 | 24 / 80

A manager asks: 'Since A has a higher overall accuracy, prove A is the better model for both easy and hard work, then route every task to A.' Their requested conclusion is a proposition to assess, not a reliable fact. There are no latency, cost, safety, or tool-use measurements in this dataset.

Calculate each model's observed accuracy within each difficulty group and overall. Assess the manager's inference, explaining the role of the different task mixes. Then compare the models using a hypothetical common workload of 50% easy and 50% hard tasks, taking the observed subgroup rates as fixed solely for this illustrative calculation. Recommend the next evaluation step needed before adopting a production-wide route, separating the observed arithmetic from statistical or causal claims the small nonrandom sample cannot establish.

# Constraints

- This is a closed-book benchmark. Use the supplied evidence and rules; do not browse, run commands, or claim external verification. Any requested code or commands are proposals, not actions to execute.
- Do not accept the claimed subgroup superiority without checking the table.
- Show denominators and use percentage values with sufficient precision.
- Use equal difficulty weights only for the specified hypothetical comparison.
- Do not infer production costs, latency, or universal future superiority from these counts.

# Evaluation criteria

1. Computes subgroup and aggregate accuracies correctly.
2. Identifies whether the requested inference follows from the evidence.
3. Explains the effect of unequal task composition.
4. Calculates the standardised comparison consistently.
5. Proposes an evaluation that addresses uncertainty and routing relevance.
