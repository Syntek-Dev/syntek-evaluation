---
benchmark: linux--systemd-analysis
version: 2
domain: linux
capability: service-startup-diagnosis
jurisdiction: UK
expected_output: analysis-and-commands
scoring: qualitative
---
# Task

A synthetic Ubuntu host runs this systemd unit:
[Service]
User=reporter
WorkingDirectory=/srv/reporting/current
ExecStart=/usr/local/bin/report-worker --config /etc/report-worker/config.toml
Restart=on-failure
RestartSec=2

After a deployment, systemctl status report-worker.service includes:
Process: 8120 ExecStart=/usr/local/bin/report-worker ... (code=exited, status=200/CHDIR)
Main PID: 8120 (code=exited, status=200/CHDIR)
Start request repeated too quickly.
The journal includes: Changing to the requested working directory failed: No such file or directory.

Read-only checks show /usr/local/bin/report-worker exists and is executable, /etc/report-worker/config.toml exists and is readable by reporter, /srv/reporting/releases/r17 exists, and /srv/reporting/current is a dangling symlink to /srv/reporting/releases/r16. The deployment record says r17 is the intended release and r16 has been removed.

Explain the causal sequence, distinguishing the initial startup failure from the later restart-limit message. Give a cautious repair and verification sequence suitable for an operator, including how to check the worker's effective user can traverse the repaired path. State whether a daemon reload is required for your chosen repair and why.

# Constraints

- This is a closed-book benchmark. Use the supplied evidence and rules; do not browse, run commands, or claim external verification. Any requested code or commands are proposals, not actions to execute.
- Do not run commands; provide a reviewable sequence with expected observations.
- Do not disable restart limits or change the service user to hide the failure.
- Preserve the intended r17 release and avoid recreating a stale release directory.
- Mark commands that change files or service state explicitly.

# Evaluation criteria

1. Identifies the original failure using both status and journal evidence.
2. Explains the relationship between the restart loop and the rate limit.
3. Repairs the deployment path without broadening privileges.
4. Checks path traversal and successful startup under the service identity.
5. Explains reload and restart requirements accurately for the proposed change.
