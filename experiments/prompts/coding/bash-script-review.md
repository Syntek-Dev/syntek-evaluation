---
benchmark: coding--bash-script-review
version: 2
domain: coding
capability: shell-production-review
jurisdiction: UK
expected_output: analysis-and-code
scoring: qualitative
---
# Task

Review and replace this fictional Bash 5.2 deployment helper. It runs as an unprivileged service user on Linux with GNU coreutils and GNU tar. An operator supplies an existing gzip tar archive as argument one. The archive is produced by a trusted build job, contains only relative paths below app/, and has no symlinks or hard links. Files must be staged before publication to /srv/widget/current. A failed extraction must leave the existing release untouched. /srv/widget/releases is on the same filesystem as current, which is a symlink. Keep prior releases for rollback.

    #!/bin/bash
    cd /srv/widget
    rm -rf current
    mkdir current
    tar xzf $1 -C current 2>/tmp/deploy.log
    echo deployed

Provide a replacement script and explain the most serious failure modes. Support paths containing spaces. Reject missing or unreadable input before changing deployment state. Print a success message only after publication, and make failure diagnostics useful without overwriting a shared predictable /tmp log. You may assume the service resolves current afresh for each request; restarting it is outside scope.

# Constraints

- This is a closed-book benchmark. Use the supplied evidence and rules; do not browse, run commands, or claim external verification. Any requested code or commands are proposals, not actions to execute.
- Use Bash and the stated GNU tools only; include strict mode and explicit checks where needed.
- Create staging and replacement symlinks with unique names; cleanup must only remove paths created by this invocation.
- Do not delete an existing release, broaden permissions, or require root.
- Mention concurrent deployment behaviour or provide a locking approach.

# Evaluation criteria

1. Prioritises destructive ordering and unchecked failure over cosmetic shell concerns.
2. Quotes input paths and checks preconditions before mutation.
3. Stages a complete release and atomically publishes the symlink.
4. Scopes cleanup safely and preserves failure diagnostics and rollback.
5. States assumptions about archive trust, filesystem semantics, and concurrency.
