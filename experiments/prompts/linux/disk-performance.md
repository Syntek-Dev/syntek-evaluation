---
benchmark: linux--disk-performance
version: 2
domain: linux
capability: storage-latency-diagnosis
jurisdiction: UK
expected_output: analysis-and-commands
scoring: qualitative
---
# Task

A synthetic batch export became slow after moving from buffered batches to calling fsync after every record. The database and export share an NVMe volume. No other deployment occurred, but that alone does not establish causation.

Over the same five-minute interval, exporter throughput fell from 8,000 to 600 records/second and its p95 request time rose from 25 ms to 420 ms. iostat for the shared device reports w_await=38 ms, aqu-sz=24, %util=99, and write throughput=75 MiB/s. Historical intervals at 500 MiB/s had w_await=3 ms. pidstat reports substantial I/O delay in exporter processes. A short application trace records roughly one fsync per completed record. The database also reports higher commit latency. There are no device errors in the supplied kernel-log excerpt. A full kernel log, device health data, and storage-provider throttling metrics have not yet been collected.

Assess the evidence and propose the next three diagnostic actions in order. Explain why low throughput can coexist with high storage latency and why device utilisation alone is insufficient to establish NVMe capacity. Propose an experiment to evaluate batching without silently changing the export's durability contract.

# Constraints

- This is a closed-book benchmark. Use the supplied evidence and rules; do not browse, run commands, or claim external verification. Any requested code or commands are proposals, not actions to execute.
- Distinguish the leading hypothesis from confirmed physical-device failure.
- Do not suggest destructive benchmarks on the live filesystem.
- Retain the requirement that acknowledged exports survive a process crash; identify any additional crash guarantees needing agreement.
- For any trace or load experiment, explain duration and production overhead controls.

# Evaluation criteria

1. Interprets latency, queue depth, throughput, and application changes together.
2. Avoids treating a single utilisation metric as definitive saturation proof.
3. Proposes diagnostics that can distinguish workload and infrastructure causes.
4. Designs a controlled and bounded comparison experiment.
5. Addresses durability and shared-database impact before changing write behavior.
