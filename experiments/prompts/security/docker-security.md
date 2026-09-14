---
benchmark: security--docker-security
version: 2
domain: security
capability: container-runtime-hardening
jurisdiction: UK
expected_output: risk-review-and-runtime-policy
scoring: qualitative
---
# Task

Review a fictional deployment for a document converter that processes customer uploads with a native parser. It runs on Linux with Docker Engine 26. The container requires read-only access to /srv/uploads for its assigned job, a writable /work directory for temporary output, and no network access. A controller outside the container uploads finished output afterward. The image already contains all required tools. Current launch configuration is:

    docker run --privileged --network host       -v /var/run/docker.sock:/var/run/docker.sock       -v /:/host       -v /srv/uploads:/input       converter:tested

The parser process currently runs as UID 0. Jobs can take up to 60 seconds and may be adversarial. The host also runs an internal model server holding confidential prompts. Recommend a replacement runtime policy or command and explain each material restriction. Include mount scope, user identity, capabilities, privilege escalation, system-call confinement, network, temporary storage, CPU/memory/process limits and job timeout. Explain what container isolation does not guarantee if the native parser is compromised, and when a stronger isolation boundary would be justified.

# Constraints

- This is a closed-book benchmark. Use the supplied evidence and rules; do not browse, run commands, or claim external verification. Any requested code or commands are proposals, not actions to execute.
- Do not mount the Docker socket, host root, or unrelated tenants into the worker.
- Use plausible example limits and label them as values requiring workload validation.
- Do not claim containers are virtual machines or that a read-only root filesystem eliminates kernel risk.
- Keep controller responsibilities outside the converter; do not introduce runtime package installation.

# Evaluation criteria

1. Identifies host-compromise paths in the supplied configuration.
2. Restricts filesystem, network and process privileges to the job needs.
3. Provides bounded resources and an external job-lifecycle control.
4. Accounts for non-root UID access and practical writable storage.
5. Explains remaining kernel/shared-host risk and stronger-boundary criteria.
