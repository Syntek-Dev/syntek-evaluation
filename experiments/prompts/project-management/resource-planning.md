---
benchmark: project-management--resource-planning
version: 2
domain: project-management
capability: capacity-allocation
jurisdiction: UK
expected_output: allocation-and-explanation
scoring: qualitative
---
# Task

Allocate one fictional working week. Engineer Ava has 24 productive hours;
engineer Ben has 20; tester Chen has 16. Hours already exclude meetings and leave.
Required work: P payment fix, 12 engineering hours by Ava only plus 4 Chen hours;
Q tenant-isolation fix, 16 engineering hours by either Ava or Ben plus 6 Chen hours;
R reporting change, 16 engineering hours by either plus 8 Chen hours; S runbook,
4 engineering hours by either, no tester. Engineering tasks are indivisible
between engineers, though a person can do multiple tasks. Testing for a task must
follow its engineering; for this weekly capacity exercise, assume sequencing
within the week is possible if assigned hours fit. P and Q are mandatory; R is
optional; S is mandatory for release. Only Chen may test. No overtime or borrowing.

The sponsor says total engineering hours nearly fit and asks to promise all four.
Produce a feasible allocation, expose each capacity constraint, calculate spare
capacity and explain what must change to deliver any deferred work. Distinguish
available engineering time from the bottleneck that limits release scope.

# Constraints

- This is a closed-book benchmark. Use the supplied evidence and rules; do not browse, run commands, or claim external verification. Any requested code or commands are proposals, not actions to execute.
- Use supplied productive hours without subtracting meetings again.
- Keep P, Q and S mandatory and do not split engineering tasks.
- Do not reassign testing to unqualified engineers.

# Evaluation criteria

1. Checks capacity by person and skill rather than only totals.
2. Preserves mandatory tasks and task assignment restrictions.
3. Provides a feasible allocation with spare hours.
4. Identifies all constraints preventing the full scope.
5. Offers an explicit scope/date/resource decision.
