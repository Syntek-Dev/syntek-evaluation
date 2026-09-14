---
benchmark: business--decision-analysis
version: 2
domain: business
capability: decision-under-constraints
jurisdiction: UK
expected_output: decision-memo
scoring: qualitative
---
# Task

A fictional platform must choose one annual hosting option. Annual commercial
costs and planning estimates are below. "Expected outage hours" are forecasts,
not guaranteed maxima. Value business interruption at £800 per hour for the
expected-cost calculation.

Option A: fee £20,000; expected outages 12 hours; no contractual recovery target.
Option B: fee £26,000; expected outages 4 hours; contractual recovery within
4 hours per incident. Option C: fee £31,000; expected outages 1 hour;
contractual recovery within 1 hour per incident. All recovery commitments are
assumed enforceable for this exercise; actual performance remains uncertain.
The board mandates a contractual recovery target no longer than 4 hours and
an annual hosting fee no higher than £28,000. The CFO prefers lowest expected
total cost. A customer manager argues that the lowest predicted downtime
automatically wins. Contract scope and exit costs have not been reviewed.

Write a decision memo showing the expected-cost calculation, feasibility against
the board's gates, and sensitivity of the economic ranking to interruption cost.
Separate the selected option from the conditions needed before signing.

# Constraints

- This is a closed-book benchmark. Use the supplied evidence and rules; do not browse, run commands, or claim external verification. Any requested code or commands are proposals, not actions to execute.
- Do not silently relax either board mandate.
- Distinguish annual expected downtime from per-incident recovery commitments.
- Use supplied forecasts without presenting them as measured reliability.

# Evaluation criteria

1. Computes expected annual costs correctly.
2. Applies mandatory gates before preference rankings.
3. Explains the difference between forecasts and commitments.
4. Provides useful sensitivity analysis with units.
5. States contractual due diligence and residual uncertainty.
