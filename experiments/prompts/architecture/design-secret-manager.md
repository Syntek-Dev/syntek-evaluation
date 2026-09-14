---
benchmark: architecture--design-secret-manager
version: 2
domain: architecture
capability: secret-management-architecture
jurisdiction: UK
expected_output: architecture-and-threat-analysis
scoring: qualitative
---
# Task

Design a fictional internal secret manager for 40 Linux services and five human administrators. Services authenticate with short-lived workload identities issued by an existing trusted identity service. A hardware-backed key service can encrypt/decrypt small data-encryption keys and emits independent audit events; its root key is non-exportable. The secret manager stores encrypted secret versions in PostgreSQL 16 and has two stateless API replicas. Workloads need read access only to explicitly assigned paths; administrators can rotate secret values but must not gain unrestricted plaintext access by default.

Requirements: rotate a database password with a ten-minute overlap of old and new credentials; make revoked workload access stop within 60 seconds; tolerate one API replica failing; recover encrypted backups in a replacement environment; never write plaintext secrets to request logs. During a key-service outage, a product manager asks that every secret remain readable indefinitely from an API cache. Evaluate that proposal against the revocation requirement.

Describe the trust boundaries, storage and key flow, access policy, rotation protocol, revocation/caching policy and recovery prerequisites. Include a concrete outage behaviour and two abuse cases. Clarify which availability properties follow from two API replicas and which depend on other components.

# Constraints

- This is a closed-book benchmark. Use the supplied evidence and rules; do not browse, run commands, or claim external verification. Any requested code or commands are proposals, not actions to execute.
- Do not invent cryptographic algorithms or store root keys beside encrypted backups.
- Use established authenticated encryption and supplied key-service capabilities at a design level.
- Do not promise both indefinite offline secret reads and enforced 60-second revocation without explaining the conflict.
- Avoid raw secret values in examples, metrics, tracing, or audit events.

# Evaluation criteria

1. Separates workload identity, authorization, encrypted storage, and key custody.
2. Designs versioned rotation and credential overlap without an unsafe cutover.
3. Resolves revocation and cache availability requirements explicitly.
4. Accounts for database, identity, key-service, and recovery dependencies.
5. Provides useful audit and abuse-case coverage without secret leakage.
