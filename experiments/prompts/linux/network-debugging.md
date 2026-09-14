---
benchmark: linux--network-debugging
version: 2
domain: linux
capability: network-path-diagnosis
jurisdiction: UK
expected_output: analysis-and-commands
scoring: qualitative
---
# Task

A synthetic Ubuntu application deployment has a reverse proxy and an API on the same host, 10.20.0.12. Clients must use HTTPS through the proxy. Direct access to the API from other hosts is prohibited. The service started returning 502 after a proxy configuration change.

Collected at the same time:
- A client resolves api.test.invalid to 10.20.0.12 and completes TLS to port 443.
- The proxy access log records that client's request and status 502.
- The proxy error log says: connect() failed (111: Connection refused) while connecting to upstream http://10.20.0.12:8080/health.
- ss -ltnp shows LISTEN 127.0.0.1:8080 owned by api, and LISTEN 0.0.0.0:443 owned by proxy.
- On the host, curl http://127.0.0.1:8080/health returns 200 and {"status":"ok"}.
- The proxy runs directly on the host, in the same network namespace as the API.

Diagnose the failing network hop. Propose the smallest configuration change consistent with the access policy, followed by commands to validate the configuration, apply it with minimal disruption, and verify recovery. Explain why the successful DNS and TLS checks do not prove the upstream path is healthy.

# Constraints

- This is a closed-book benchmark. Use the supplied evidence and rules; do not browse, run commands, or claim external verification. Any requested code or commands are proposals, not actions to execute.
- Use only these observations; do not assume a container, firewall rule, or DNS outage.
- Preserve the requirement that the API is reachable only through the proxy.
- Separate read-only diagnosis from configuration changes and service reloads.
- For each proposed command, explain the expected evidence rather than claiming to have executed it.

# Evaluation criteria

1. Localises the failure to a specific connection using the supplied evidence.
2. Relates listening addresses to the configured upstream address.
3. Proposes a minimal correction that preserves the access policy.
4. Gives a practical validation and recovery sequence.
5. Distinguishes demonstrated facts from untested alternative causes.
