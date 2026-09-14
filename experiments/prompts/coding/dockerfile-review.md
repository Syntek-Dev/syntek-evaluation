---
benchmark: coding--dockerfile-review
version: 2
domain: coding
capability: container-build-review
jurisdiction: UK
expected_output: analysis-and-dockerfile
scoring: qualitative
---
# Task

A fictional Python 3.12 HTTP service listens on port 8080 and runs with python -m widget. It writes temporary request files only under /tmp, never installs packages at runtime, and handles SIGTERM directly. The build context contains source, requirements.lock, .env, and a .git directory. requirements.lock lists all direct and transitive dependencies with exact versions and hashes; dependencies are pure Python wheels. CI supplies a tested base image reference including its sha256 digest through a build argument.

    FROM python:latest
    WORKDIR /app
    COPY . .
    RUN pip install -r requirements.lock
    ENV API_TOKEN=change-me
    EXPOSE 8080
    CMD python -m widget

Review reproducibility, secret exposure, caching, permissions, and shutdown. Provide a corrected Dockerfile, a .dockerignore, and concise build/run notes for CI. The final process must use a non-root UID and work with a read-only root filesystem when /tmp is a bounded writable mount. Explain what a pinned build can and cannot establish about dependency safety.

# Constraints

- This is a closed-book benchmark. Use the supplied evidence and rules; do not browse, run commands, or claim external verification. Any requested code or commands are proposals, not actions to execute.
- Treat package/image references as fixture inputs; do not invent an actual image digest or claim a vulnerability scan.
- Use pip hash verification and avoid embedding runtime secrets in image layers or build arguments.
- Use the service module directly with an exec-form command; do not introduce an unneeded process manager.

# Evaluation criteria

1. Makes the base image and dependencies reproducible using supplied inputs.
2. Excludes local secrets and unrelated repository contents from the build context.
3. Improves cache boundaries and limits runtime write permissions.
4. Preserves signal delivery and supports the stated runtime filesystem constraints.
5. Explains residual security and maintenance responsibilities accurately.
