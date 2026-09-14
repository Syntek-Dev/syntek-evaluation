---
benchmark: debugging--docker-container-failure
version: 2
domain: debugging
capability: container-lifecycle-diagnosis
jurisdiction: UK
expected_output: diagnosis-and-remediation
scoring: qualitative
---
# Task

A fictional Docker Engine 26 deployment runs a Python 3.12 queue worker. The image builds successfully, but its container repeatedly exits with code 0 and is restarted by an external supervisor. The worker itself logs "ready" when started interactively. The final image instruction is:

    CMD ["sh", "-c", "python -m widget.worker &"]

Observed events in order:
container start 11:40:00.100
worker stdout: ready 11:40:00.140
container die exitCode=0 11:40:00.145
container restart 11:40:01.000
No OOM event, Python traceback, missing-module error, or failing health check appears. The worker normally blocks while waiting for jobs and handles SIGTERM to stop accepting work, finish its current job within 20 seconds, and exit. Deployment shutdown grace is currently five seconds.

Diagnose the lifecycle problem and provide the corrected image command and a proposed shutdown-grace setting with rationale. Explain how to verify signal delivery, normal idle behaviour, and graceful termination without assuming that an exit code of zero always means a healthy service. Also state what evidence would be needed before pursuing a separate Python crash hypothesis.

# Constraints

- This is a closed-book benchmark. Use the supplied evidence and rules; do not browse, run commands, or claim external verification. Any requested code or commands are proposals, not actions to execute.
- Do not add an infinite sleep, tail -f, or a second unrelated foreground process to keep the container alive.
- Do not change credentials, network ports, or memory limits without supporting evidence.
- Use the declared worker behaviour and distinguish build success from runtime correctness.
- Describe tests as proposed; do not claim the container was executed.

# Evaluation criteria

1. Connects the backgrounded worker and exiting shell to container lifecycle.
2. Supplies an exec-form foreground process command.
3. Accounts for SIGTERM delivery and the worker completion bound.
4. Verifies readiness, idle persistence, and graceful stop separately.
5. Avoids speculative fixes unsupported by the event sequence.
