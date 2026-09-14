---
benchmark: linux--inode-exhaustion
version: 2
domain: linux
capability: inode-exhaustion-diagnosis
jurisdiction: UK
expected_output: analysis-and-commands
scoring: qualitative
---
# Task

A synthetic worker fails to create /srv/spool/jobs/new/job-4103 with No space left on device. Its spool is a dedicated ext4 filesystem. df -h /srv/spool reports 200 GiB total, 40 GiB used, and 150 GiB available. df -i /srv/spool reports 3,000,000 inodes, 3,000,000 used, and 0 free. Directory counts from the application's existing manifest show 2.9 million tiny files under jobs/completed and 30,000 files under jobs/new; other inodes account for the remainder.

Application policy allows deletion only of completed files whose recorded completion time is more than seven days old. Files in jobs/new or jobs/running must never be deleted by maintenance. The manifest includes exact relative paths and completion timestamps and is authoritative for lifecycle state, but filenames may contain spaces, tabs, or newlines. New job intake can be paused without terminating running jobs. The retention cleanup was disabled three weeks ago; no evidence indicates block corruption.

Explain the immediate failure and outline a safe recovery sequence that creates enough inode headroom to resume intake. Include dry-run accounting, race handling, bounded deletion, monitoring, and a prevention strategy. State what storage redesign might help if the expected steady-state file count exceeds available inodes.

# Constraints

- This is a closed-book benchmark. Use the supplied evidence and rules; do not browse, run commands, or claim external verification. Any requested code or commands are proposals, not actions to execute.
- Do not delete active jobs or select candidates solely by a filename pattern.
- Respect the seven-day retention rule and distinguish completion time from filesystem mtime.
- Handle unusual filenames safely and keep deletion batches bounded.
- Treat any filesystem reformat or data migration as a separate planned operation.

# Evaluation criteria

1. Distinguishes inode capacity from byte capacity using the supplied metrics.
2. Selects deletion candidates according to the lifecycle and retention policy.
3. Accounts for races and unsafe filename handling.
4. Defines recovery checks and a controlled resume condition.
5. Proposes monitoring and architectural prevention proportional to the evidence.
