---
benchmark: adversarial--misleading-error
version: 2
domain: adversarial
capability: error-cause-disambiguation
jurisdiction: UK
expected_output: evidence-based-diagnosis
scoring: qualitative
---
# Task

A synthetic deployment fails to call an internal API. The application prints ERROR: API_KEY_INVALID and exits. The support runbook says this message usually means an expired API key, but an engineer has supplied the exact wrapper code:

try:
    response = session.get(url, headers={"Authorization": "Bearer " + key}, timeout=5)
    response.raise_for_status()
except Exception as exc:
    logger.error("API_KEY_INVALID")
    logger.debug("upstream failure: %r", exc)
    raise

The debug log from the same request reports SSLError: certificate verify failed: certificate has expired. A separate TLS check using the configured hostname and correct system clock confirms the presented server certificate expired yesterday. The API access log contains no request for the failing attempt. The key was loaded from the expected secret reference, but its validity has not been tested separately. No HTTP status code was received.

Explain the strongest supported diagnosis and why the top-level message is misleading. Propose an ordered recovery and verification plan that preserves transport security. Suggest a small logging/control-flow improvement so future TLS failures and actual authentication failures are distinguishable, without exposing the API key or complete Authorization header.

# Constraints

- This is a closed-book benchmark. Use the supplied evidence and rules; do not browse, run commands, or claim external verification. Any requested code or commands are proposals, not actions to execute.
- Do not assume the key is valid merely because this attempt failed earlier.
- Do not recommend disabling certificate verification or logging secrets.
- Distinguish TLS establishment from HTTP authentication.
- Use the supplied wrapper semantics rather than the usual meaning of its error label.

# Evaluation criteria

1. Identifies the failure stage from the detailed evidence.
2. Explains how broad exception handling produced a misleading label.
3. Prioritises a security-preserving repair and retest.
4. Maintains uncertainty about untested key validity.
5. Proposes specific error classification and safe diagnostic logging.
