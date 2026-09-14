---
benchmark: linux--permissions
version: 2
domain: linux
capability: filesystem-access-diagnosis
jurisdiction: UK
expected_output: analysis-and-commands
scoring: qualitative
---
# Task

A synthetic service runs as user invoice, primary group invoice, and supplemental group billing. It needs to read /srv/billing/exports/september.csv. Opening the file fails with Permission denied. These are the effective filesystem facts; there are no ACLs, no security-module denials, no systemd path restrictions, and no unusual mount options.

namei -l /srv/billing/exports/september.csv shows:
drwxr-xr-x root root /
drwxr-xr-x root root srv
drwx------ root root billing
drwxr-x--- root billing exports
-rw-r----- root billing september.csv

The running process's /proc/PID/status Groups field includes the numeric billing group ID. The file is not executable and does not need to be. The owner requires that unrelated local users cannot list or traverse /srv/billing, while the invoice account and existing billing group members must be able to traverse it. Listing the contents of /srv/billing itself is not required. Ownership of the CSV and exports directory should remain unchanged.

Identify the blocked permission check. Give a minimal group-based repair and a read-only validation under the service identity. Explain the roles of directory read and execute permissions and whether adding file execute permission or restarting the already-correctly-grouped service would help.

# Constraints

- This is a closed-book benchmark. Use the supplied evidence and rules; do not browse, run commands, or claim external verification. Any requested code or commands are proposals, not actions to execute.
- Apply least privilege using ordinary Unix owner/group/mode permissions.
- Do not use recursive chmod/chown, world-readable permissions, or running as root.
- Explain the effect of each proposed mutation before listing validation.
- Do not infer additional policy mechanisms excluded by the scenario.

# Evaluation criteria

1. Identifies the exact path component that blocks traversal.
2. Distinguishes directory search permission from file read permission.
3. Produces a narrowly scoped repair satisfying the access rules.
4. Validates access using the effective service identity.
5. Rejects unrelated permission and restart changes with clear reasons.
