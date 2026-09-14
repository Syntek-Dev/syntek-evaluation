---
benchmark: coding--python-write-tests
version: 2
domain: coding
capability: test-design
jurisdiction: UK
expected_output: tests-and-rationale
scoring: qualitative
---
# Task

Write pytest tests for a fictional Python 3.12 retry helper. Its contract and implementation are below; assess the implementation without modifying it. Only TransientError is retried. attempts includes the first call and must be at least one. Between failed attempts, sleep for base_delay * 2**failure_index, with failure_index starting at zero. Never sleep after the last failed attempt. Return any successful result, including None. Raise ValueError before calling send or sleep when attempts < 1 or base_delay < 0. Propagate the final original exception instance. The send and sleep callables are supplied so tests need neither a network nor real waiting.

    class TransientError(Exception):
        pass

    def retry(send, sleep, attempts=3, base_delay=0.1):
        for n in range(attempts):
            try:
                return send()
            except Exception:
                sleep(base_delay * 2**n)
        raise RuntimeError('failed')

Assume this code lives in retrying.py. Supply a compact test module, explain which tests fail for substantive reasons, and identify any ambiguity you would clarify before testing beyond the specified contract.

# Constraints

- This is a closed-book benchmark. Use the supplied evidence and rules; do not browse, run commands, or claim external verification. Any requested code or commands are proposals, not actions to execute.
- Use pytest and ordinary fakes; no real sleeps, network calls, or timing assertions.
- Do not make assertions depend on private loop variables or a rewritten implementation.
- Keep exception identity checks separate from matching an error message; do not invent message requirements.

# Evaluation criteria

1. Covers successful returns, transient recovery, and exhaustion with observable assertions.
2. Distinguishes retriable exceptions from permanent exceptions.
3. Verifies delay sequence and absence of unnecessary sleeping.
4. Tests input validation and absence of side effects for invalid inputs.
5. Explains demonstrated defects without claiming the tests were executed.
