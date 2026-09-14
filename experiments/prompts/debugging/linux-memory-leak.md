---
benchmark: debugging--linux-memory-leak
version: 2
domain: debugging
capability: memory-diagnosis
jurisdiction: UK
expected_output: diagnosis-and-investigation
scoring: qualitative
---
# Task

A fictional Linux service runs Python 3.12 inside a cgroup v2 memory limit of 1 GiB. It periodically reads a 600 MiB immutable data file into a request-local buffer, computes a digest, and releases the buffer. After one job, the dashboard labels 870 MiB as "used". An operator proposes restarting the service every hour because this proves a Python memory leak.

Measurements after the job and after 20 minutes idle:
process VmRSS: 210 MiB -> 212 MiB
cgroup memory.current: 870 MiB -> 872 MiB
memory.stat anon: 205 MiB -> 207 MiB
memory.stat file: 620 MiB -> 620 MiB
memory.stat kernel: 45 MiB -> 45 MiB
memory.events: low=0 high=0 max=0 oom=0 oom_kill=0
The dashboard plots memory.current. Ten earlier completed jobs returned to approximately the same idle values; no latency regression is reported.

Assess the claim, explain the measurements, and give a staged investigation if the next ten jobs start increasing idle anonymous memory. Include what you would measure before and after representative workloads and what would justify mitigation. Explain the limits of Python allocation tracing for native allocations.

# Constraints

- This is a closed-book benchmark. Use the supplied evidence and rules; do not browse, run commands, or claim external verification. Any requested code or commands are proposals, not actions to execute.
- Do not declare either a proven leak or unlimited memory safety from this snapshot.
- Do not propose dropping host caches, disabling the limit, or scheduled restarts as the first diagnostic step.
- Use the stated cgroup v2 accounting and MiB units; no tool execution is available.
- Separate process memory, file cache, allocator retention, and genuinely retained live objects.

# Evaluation criteria

1. Interprets the dashboard using the supplied memory categories.
2. Uses repeated idle baselines and OOM evidence appropriately.
3. States uncertainty and avoids conflating resident cache with a proven leak.
4. Proposes workload-correlated measurements with useful escalation criteria.
5. Explains Python/native allocation visibility and safe mitigation tradeoffs.
