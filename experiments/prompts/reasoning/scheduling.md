---
benchmark: reasoning--scheduling
version: 2
domain: reasoning
capability: precedence-constrained-scheduling
jurisdiction: UK
expected_output: schedule-and-lower-bound
scoring: qualitative
---
# Task

Two identical workers must execute six synthetic maintenance tasks. Each task needs exactly one worker for its full duration, cannot be paused, and cannot be split. Workers are available from time zero. Handoffs and task starts take no time, and a task may start at the exact instant all predecessors finish. A worker can do any task. The units below are hours, and intervals should be written as [start,end).

Task | Duration | Required completed predecessors
A | 3 | none
B | 2 | none
C | 4 | A
D | 2 | A
E | 3 | B
F | 2 | C, D, E

No task consumes any other shared resource, and workers may be idle. The objective is to minimise the finish time of all tasks, including F. The manager suggests immediately assigning both C and D after A finishes, without explaining where E will fit.

Produce one optimal schedule with a worker, start, and finish for every task. Check predecessor ordering and worker overlap explicitly. Show a lower bound on completion time and explain why your schedule meets it. Assess whether the manager's suggestion necessarily yields an optimal schedule, taking the prior placement of E into account.

# Constraints

- This is a closed-book benchmark. Use the supplied evidence and rules; do not browse, run commands, or claim external verification. Any requested code or commands are proposals, not actions to execute.
- Use the given durations and two-worker limit exactly; do not add workers or overlap tasks on one worker.
- Include idle intervals where needed for clarity.
- Provide a proof of minimal makespan rather than only a plausible ordering.
- Treat any distinct schedule meeting the same proven optimum as equally acceptable.

# Evaluation criteria

1. Builds a complete schedule satisfying all dependencies.
2. Checks worker capacity and interval boundary semantics.
3. Computes the makespan and a valid independent lower bound.
4. Shows that the lower bound is attained.
5. Analyses the manager suggestion without assuming omitted schedule details.
