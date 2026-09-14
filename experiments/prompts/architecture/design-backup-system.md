---
benchmark: architecture--design-backup-system
version: 2
domain: architecture
capability: backup-recovery-design
jurisdiction: UK
expected_output: recovery-plan-and-calculations
scoring: qualitative
---
# Task

A fictional UK SaaS service stores 4 TB of PostgreSQL data, where TB means 10^12 bytes. It takes a nightly base backup and ships write-ahead logs every five minutes to an independent storage account. The stated objectives are RPO at most 15 minutes and RTO at most six hours after total loss of the primary site. The only currently documented recovery link from backup storage to a replacement site is 200 Mbit/second, where Mbit means 10^6 bits. For the minimum-time calculation ignore compression, protocol overhead, WAL replay and provisioning; then discuss why real recovery is slower. The service also stores 600 GB of uploaded objects, whose backup process has not been documented.

Assess whether the documented design establishes either objective. Calculate the minimum time to transfer the database and the minimum ideal link rate needed to transfer it within six hours. Propose a recoverable design and a restore exercise with evidence to collect. Include consistency between database rows and uploaded objects, backup-account compromise, encryption-key recovery, retention, and verification of a successful application-level restore. The budget allows one additional recovery copy but no assumption of an already-running second production site.

# Constraints

- This is a closed-book benchmark. Use the supplied evidence and rules; do not browse, run commands, or claim external verification. Any requested code or commands are proposals, not actions to execute.
- Do not equate a completed backup job with a demonstrated successful restore.
- Use decimal units for the supplied arithmetic and show bit/byte conversion.
- Keep RPO and RTO distinct; note missing evidence about WAL continuity and object backups.
- Do not claim a nightly base backup alone gives a 15-minute RPO.

# Evaluation criteria

1. Calculates transfer limits correctly and identifies the RTO constraint.
2. Assesses RPO from continuous recoverability rather than schedule alone.
3. Includes object consistency, keys, isolation and corruption/compromise recovery.
4. Proposes a practical additional-copy strategy within the stated scope.
5. Defines timed restore validation and meaningful success evidence.
