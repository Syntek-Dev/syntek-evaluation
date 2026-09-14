---
benchmark: debugging--linux-high-cpu
version: 2
domain: debugging
capability: cpu-root-cause
jurisdiction: UK
expected_output: diagnosis-and-code
scoring: qualitative
---
# Task

A fictional Python 3.12 worker on a four-core Linux host uses almost one full core after a credential rotation. Its queue is empty. A 30-second profile attributes 91% of on-CPU samples to the loop below and exception/log formatting; the network calls return in under 1 ms. Logs repeat "poll failed: 401 invalid token" about 8,000 times per second. Process CPU is 99%, host aggregate CPU is 26%, I/O wait is 0.3%, and memory is stable.

    while True:
        try:
            job = client.poll()
            if job is not None:
                process(job)
        except Exception as exc:
            logger.error('poll failed: %s', exc)
            continue

The fictional client raises AuthError for 401, TemporaryError for retryable failures, and returns None when no job is available. process failures must be reported to the queue failure handler and must not be confused with polling failures. Propose a corrected control flow and an operational recovery sequence. Include bounded retry delays, shutdown responsiveness, and a way to prevent a log flood without hiding persistent failure.

# Constraints

- This is a closed-book benchmark. Use the supplied evidence and rules; do not browse, run commands, or claim external verification. Any requested code or commands are proposals, not actions to execute.
- Do not increase CPU limits or add workers before addressing the evidenced loop.
- Use injected wait/stop controls in sample code so the design is testable without real waiting.
- Do not catch and suppress cancellation or process-termination signals.
- Do not log credentials, tokens, or complete remote response bodies.

# Evaluation criteria

1. Uses the profile and error rate to identify the busy retry loop.
2. Interprets process versus host CPU percentages coherently.
3. Separates permanent authentication, transient polling, idle polling, and job-processing cases.
4. Provides bounded, interruptible retry behaviour and proportionate logging.
5. Describes credential recovery and verification without claiming the replacement is already deployed.
