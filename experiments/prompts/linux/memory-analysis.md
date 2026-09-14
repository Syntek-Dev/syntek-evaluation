---
benchmark: linux--memory-analysis
version: 2
domain: linux
capability: cgroup-memory-diagnosis
jurisdiction: UK
expected_output: analysis-and-commands
scoring: qualitative
---
# Task

A synthetic Ubuntu host has 32 GiB RAM and runs a document worker under cgroup v2. The service is periodically killed, but a dashboard says the host still has plenty of free memory. All values below are contemporaneous and GiB means 2^30 bytes.

free -h reports MemAvailable=20 GiB. The service unit has MemoryMax=4G. In its cgroup, memory.max=4294967296, memory.current=4261412864 immediately before the event, and memory.swap.max=0. Across the event, memory.events changes from oom=7, oom_kill=4 to oom=8, oom_kill=5. The kernel log identifies a memory-cgroup out-of-memory kill of the worker. A recent memory.stat sample attributes approximately 3.7 GiB to anon and 0.2 GiB to file. Request concurrency rose from four to sixteen that morning; no per-request memory measurements are available. RSS falls when a fresh worker starts, but no steady-load trend has been measured.

Explain why host-level available memory does not contradict this event. Provide a prioritised collection plan and short-term mitigation options, including how to distinguish a leak from higher concurrency or larger inputs. Describe what would justify changing the memory limit.

# Constraints

- This is a closed-book benchmark. Use the supplied evidence and rules; do not browse, run commands, or claim external verification. Any requested code or commands are proposals, not actions to execute.
- Treat the logs and counter deltas as evidence; do not claim a leak is proven.
- Do not recommend host-wide cache dropping, disabling OOM protection, or unbounded memory.
- State the operational tradeoffs of each mitigation.
- Keep commands read-only except clearly labelled optional mitigations.

# Evaluation criteria

1. Explains the interaction between host memory and the service limit.
2. Uses event deltas and the kernel attribution correctly.
3. Distinguishes anonymous memory, file cache, and incomplete attribution.
4. Proposes measurements that separate competing growth explanations.
5. Offers bounded mitigations with capacity and availability considerations.
