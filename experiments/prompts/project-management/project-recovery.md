---
benchmark: project-management--project-recovery
version: 2
domain: project-management
capability: recovery-planning
jurisdiction: UK
expected_output: recovery-plan
scoring: qualitative
---
# Task

A fictional project is at the start of working day 16. The fixed target is the
end of day 25, leaving 10 full working days including today. Remaining work:
A access fix, 3 engineer-days; B integration, 5 engineer-days after A; C test,
3 tester-days after B; D handover, 1 operations-day after C. One engineer, one
tester and one operations owner are available. Activities occupy full working
days, are non-preemptive and sequential where dependencies require. A and C are
mandatory safety gates. Scope option: a sponsor-approved reduced integration
would make B 3 days, with all other durations unchanged. The sponsor has not
approved it yet. A second engineer is available at extra cost, but the given
estimates assume the work cannot be divided or accelerated by adding people.

Prepare a recovery note showing the current earliest finish, the reduced-scope
finish and the decision needed today. Include an honest stakeholder update,
revised milestones and daily recovery controls. Explain why reported percentage
complete or added headcount alone does not resolve the remaining dependency chain.

# Constraints

- This is a closed-book benchmark. Use the supplied evidence and rules; do not browse, run commands, or claim external verification. Any requested code or commands are proposals, not actions to execute.
- Count day 16 as the first available day and show inclusive activity dates.
- Do not skip safety gates, overlap dependent work or assume overtime.
- Label the reduced-scope schedule as conditional on approval.

# Evaluation criteria

1. Calculates remaining duration and finish dates consistently.
2. Identifies the true sequential bottleneck.
3. Evaluates the proposed scope and staffing options.
4. Makes a clear decision request and honest stakeholder update.
5. Defines realistic milestones and recovery monitoring.
