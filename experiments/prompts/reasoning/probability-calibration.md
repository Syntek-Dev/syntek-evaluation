---
benchmark: reasoning--probability-calibration
version: 2
domain: reasoning
capability: base-rate-and-dependence
jurisdiction: UK
expected_output: probability-calculation-and-uncertainty
scoring: qualitative
---
# Task

A fictional factory uses a binary sensor to flag defective widgets. This is a quality-control exercise, not a medical or financial decision. For a batch of exactly 10,000 widgets, exactly 2% are defective. The supplied sensor model flags exactly 90% of defective widgets and exactly 5% of non-defective widgets in this batch. Treat these rates as exact frequencies for the first calculation. All widgets are tested once, with no missing results.

A manager says, 'A flagged widget has a 90% chance of being defective, because the sensor catches 90% of defects.' A second manager proposes testing each flagged widget again with the same sensor and multiplying false-positive probabilities, claiming that two flags settle the question. No data about conditional dependence between repeat readings, drift, or widget-specific sensor errors are supplied. In a future batch, defect prevalence might differ from 2%.

Build a confusion table and calculate the probability a flagged widget is defective and the probability an unflagged widget is defective. Evaluate both managers' claims. Explain what additional evidence is needed to estimate the probability after two flags and how changing prevalence would affect the meaning of a single flag if sensitivity and false-positive rate remained fixed.

# Constraints

- This is a closed-book benchmark. Use the supplied evidence and rules; do not browse, run commands, or claim external verification. Any requested code or commands are proposals, not actions to execute.
- Show natural-frequency counts before probabilities and label each denominator.
- Report percentages to two decimal places, retaining sufficient precision internally.
- Do not assume repeated sensor readings are conditionally independent.
- Keep exact within-batch calculations separate from uncertain extrapolation to future batches.

# Evaluation criteria

1. Constructs a consistent confusion table from prevalence and sensor rates.
2. Calculates both requested conditional probabilities with correct denominators.
3. Distinguishes sensitivity from positive predictive probability.
4. Explains why repeat-reading dependence prevents an unsupported second posterior.
5. Describes prevalence effects and limits of transferring the batch result.
