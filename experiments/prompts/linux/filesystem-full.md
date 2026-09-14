---
benchmark: linux--filesystem-full
version: 2
domain: linux
capability: disk-space-accounting
jurisdiction: UK
expected_output: analysis-and-commands
scoring: qualitative
---
# Task

A synthetic Ubuntu host refuses new writes to /var/log with No space left on device. The filesystem mounted on /var/log is a dedicated 100 GiB ext4 volume. df -h reports 100 GiB used and 0 available; df -i reports only 8% of inodes used. du -xsh /var/log, run with sufficient permissions, reports 6 GiB. The measurements use comparable units and were taken within one minute during stable load.

lsof +L1 shows PID 2410, command ingest, FD 7w, size 100931731456 bytes, name /var/log/ingest/events.log (deleted), on that same filesystem. The service's documented SIGHUP handler closes its current log descriptor and reopens the configured log path. The service supervisor and PID were verified, and a correctly owned empty replacement events.log already exists. There is no application durability requirement for the deleted diagnostic log; the on-call operator has already captured the necessary incident excerpt.

Explain the discrepancy between df and du and propose the smallest recovery action supported by the supplied service behavior. Give preflight and post-recovery checks, including how to verify the file descriptor was released. Explain why deleting more small files, rebooting, or focusing on inode capacity would be poor first steps.

# Constraints

- This is a closed-book benchmark. Use the supplied evidence and rules; do not browse, run commands, or claim external verification. Any requested code or commands are proposals, not actions to execute.
- Use the stated log-reopen contract; do not assume every service handles SIGHUP this way.
- Clearly label any signal or filesystem mutation.
- Do not truncate arbitrary /proc descriptors or delete unrelated files.
- Include recurrence prevention tied to log rotation and descriptor reopening.

# Evaluation criteria

1. Explains how an unlinked open file affects block accounting.
2. Uses inode and file-size evidence to prioritise the diagnosis.
3. Chooses a minimal recovery with appropriate identity checks.
4. Verifies both descriptor release and filesystem space recovery.
5. Provides prevention relevant to the established cause.
