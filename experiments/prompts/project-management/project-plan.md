---
benchmark: project-management--project-plan
version: 2
domain: project-management
capability: critical-path-planning
jurisdiction: UK
expected_output: plan-and-schedule
scoring: qualitative
---
# Task

Plan a fictional portal pilot starting at time t=0. Durations are whole working
days; an activity finishing at t=n allows its successor to start at t=n. Tasks:
A requirements (2 days, analyst); B access design (3 days, security, after A);
C sandbox build (4 days, engineer, after A); D integration (3 days, engineer,
after B and C); E acceptance test (2 days, client, after D); F training (1 day,
analyst, after C); G go/no-go (1 day, sponsor, after E and F). Each named role
has one available person; roles are different people. Tasks are non-preemptive.
Sponsor asks whether completion by t=11 is feasible. There are no holidays,
extra staff, overtime or partial approvals. Production rollout is out of scope.

Produce a dependency-based schedule with start/finish times, the critical path,
role ownership, milestones and a concise risk register. Explain the earliest
completion time and identify an explicit decision if the sponsor's target cannot
be met. Distinguish a schedule derived from the given durations from certainty
that estimates will hold in practice.

# Constraints

- This is a closed-book benchmark. Use the supplied evidence and rules; do not browse, run commands, or claim external verification. Any requested code or commands are proposals, not actions to execute.
- Respect all dependencies, role capacity and the finish-to-start convention.
- Do not silently shorten tasks or omit go/no-go.
- Use relative working-day times, not calendar dates.

# Evaluation criteria

1. Builds a feasible dependency and resource schedule.
2. Identifies the critical path and earliest completion.
3. Evaluates the sponsor target honestly.
4. Includes meaningful owners, milestones and risks.
5. Explains estimate uncertainty and change options.
