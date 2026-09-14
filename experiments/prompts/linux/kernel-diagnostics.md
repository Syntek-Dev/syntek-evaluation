---
benchmark: linux--kernel-diagnostics
version: 2
domain: linux
capability: kernel-log-causal-analysis
jurisdiction: UK
expected_output: analysis-and-commands
scoring: qualitative
---
# Task

A synthetic Ubuntu host reports an application write failure at 14:02:11 UTC. The service logs EROFS while writing /srv/data/orders.tmp. Selected kernel messages are:
14:02:09 nvme nvme1: I/O 871 QID 3 timeout, aborting
14:02:10 blk_update_request: I/O error, dev nvme1n1, sector 921600
14:02:10 EXT4-fs error (device nvme1n1): ext4_journal_check_start: Detected aborted journal
14:02:10 EXT4-fs (nvme1n1): Remounting filesystem read-only
14:02:11 app-worker: write failed

findmnt /srv/data identifies source /dev/nvme1n1, type ext4, and options ro,relatime. Root and application binaries live on a different device and remain healthy. A backup snapshot from 02:00 UTC exists, but its restore has not been tested. The database using /srv/data is still accepting read requests; application writes should be paused during the incident. No device health report or complete surrounding kernel log has yet been collected.

Explain the sequence and what it does and does not establish about root cause. Give an ordered containment and evidence plan, then describe the conditions for filesystem repair or restore. Explain why repeatedly remounting read-write, rebooting immediately, or running filesystem repair on the mounted live volume could worsen the incident.

# Constraints

- This is a closed-book benchmark. Use the supplied evidence and rules; do not browse, run commands, or claim external verification. Any requested code or commands are proposals, not actions to execute.
- Preserve evidence and separate read-only collection from downtime-requiring recovery.
- Do not assert that physical hardware failure is proven by this excerpt.
- Do not prescribe a forced mounted-filesystem repair.
- Include data integrity and backup validation before resuming writes.

# Evaluation criteria

1. Connects the application error to the kernel and mount evidence.
2. Orders containment before potentially destructive recovery.
3. Distinguishes storage-path evidence from an established hardware diagnosis.
4. Gives a safe offline-repair or restore decision process.
5. Defines integrity and operational checks needed before write recovery.
