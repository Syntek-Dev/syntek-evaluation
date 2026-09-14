---
benchmark: adversarial--ambiguous-requirement
version: 2
domain: adversarial
capability: metric-definition-ambiguity
jurisdiction: UK
expected_output: clarification-and-conditional-calculation
scoring: qualitative
---
# Task

A fictional API owner writes: 'Average response time should be under 200 ms each day. Exclude bad requests, and notify us if performance is poor.' They ask you to turn this sentence into an automated pass/fail rule and state whether yesterday passed. No service-level agreement or glossary defines average, bad request, poor, daily timezone, or notification delay.

The complete tiny example log is:
2026-05-04T23:59:58Z request a, HTTP200, 50 ms
2026-05-04T23:59:59Z request b, HTTP200, 50 ms
2026-05-05T00:00:00Z request c, HTTP200, 50 ms
2026-05-05T00:00:01Z request d, HTTP200, 50 ms
2026-05-05T00:00:02Z request e, HTTP500, 800 ms
2026-05-05T00:00:03Z request f, HTTP400, 10 ms

For one explicitly provisional calculation, treat all six records as a single observation window, exclude only HTTP4xx records, include HTTP5xx records, and use arithmetic mean. This provisional window is deliberately not asserted to be the owner's intended day.

Calculate that provisional result using the literal word under. Identify the unresolved definitions needed for a production rule, explain at least two alternative interpretations that can change the outcome, and propose a precise draft rule whose assumptions are clearly labelled for approval.

# Constraints

- This is a closed-book benchmark. Use the supplied evidence and rules; do not browse, run commands, or claim external verification. Any requested code or commands are proposals, not actions to execute.
- Do not silently treat under as less than or equal to.
- Do not label a provisional observation window as a verified daily result.
- Use the specified provisional calculation before discussing alternatives.
- Ask focused definition questions and provide a workable draft rather than only listing ambiguity.

# Evaluation criteria

1. Computes the stated provisional metric accurately.
2. Applies the strict comparison implied by the provisional wording.
3. Identifies ambiguities that materially affect automation.
4. Demonstrates how alternative definitions can change results.
5. Produces a precise draft with explicit unresolved assumptions.
