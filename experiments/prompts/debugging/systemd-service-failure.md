---
benchmark: debugging--systemd-service-failure
version: 2
domain: debugging
capability: service-startup-diagnosis
jurisdiction: UK
expected_output: diagnosis-and-remediation
scoring: qualitative
---
# Task

A fictional Linux host with systemd 255 cannot start widget.service. Its unit and observations are:

    [Service]
    User=widget
    Group=widget
    WorkingDirectory=/srv/widget
    ExecStart=/srv/widget/.venv/bin/python -m widget
    Restart=on-failure

journal: Failed at step EXEC spawning /srv/widget/.venv/bin/python: Permission denied
systemctl status: status=203/EXEC
namei -l /srv/widget/.venv/bin/python:
  /                  drwxr-xr-x root root
  srv                drwxr-xr-x root root
  widget             drwxr-xr-x root widget
  .venv              drwx------ root root
  bin                drwxr-xr-x root root
  python             -rwxr-xr-x root root
The executable is a valid ELF binary; the mount permits execution. An interactive root invocation succeeds. No mandatory-access-control denial is recorded for this attempt.

Give a diagnosis tied to the path traversal evidence, a least-privilege repair, and steps to validate startup as the service identity. Explain why running the service as root or recursively applying mode 777 would be inappropriate. State when daemon-reload would be relevant and how to avoid a rapid restart loop while investigating.

# Constraints

- This is a closed-book benchmark. Use the supplied evidence and rules; do not browse, run commands, or claim external verification. Any requested code or commands are proposals, not actions to execute.
- Treat listed modes and unit values as complete for the immediate failure; do not invent missing packages.
- Do not make application files writable by every user or unnecessarily change ownership of the whole tree.
- Show proposed commands and relevant checks without claiming execution.
- Preserve User=widget and Group=widget.

# Evaluation criteria

1. Connects 203/EXEC and permission denial to the inaccessible path component.
2. Explains why root success does not establish service-user access.
3. Repairs traversal rights using limited ownership/group or ACL changes.
4. Validates the service identity and successful application readiness.
5. Handles systemd reload/restart semantics and restart-loop control accurately.
