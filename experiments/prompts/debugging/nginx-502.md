---
benchmark: debugging--nginx-502
version: 2
domain: debugging
capability: reverse-proxy-diagnosis
jurisdiction: UK
expected_output: diagnosis-and-remediation
scoring: qualitative
---
# Task

A fictional Linux host runs Nginx 1.24 and a Python application as separate systemd services in the same network namespace. After a deployment, GET /health returns 502. The deployment changed the application listen port. All observations below were taken during the same minute:

nginx config: location / { proxy_pass http://127.0.0.1:8000; }
nginx error: connect() failed (111: Connection refused) while connecting to upstream, upstream: "http://127.0.0.1:8000/health"
app journal: serving on http://127.0.0.1:8080
ss -ltnp: LISTEN 127.0.0.1:8080 users:(("python",pid=4412,fd=6))
curl http://127.0.0.1:8080/health: HTTP/1.1 200 OK, body {"ok":true}
nginx access: request_id=ab7 status=502 upstream_status=502

Explain the most likely immediate fault and which observations support it. Provide a minimally disruptive correction with validation and rollback, then identify two checks you would make if the same 502 persisted after that correction. The service is not containerised and there is no load balancer or service mesh in this fixture. An operator can edit configuration and reload Nginx but cannot afford an unexplained broad restart.

# Constraints

- This is a closed-book benchmark. Use the supplied evidence and rules; do not browse, run commands, or claim external verification. Any requested code or commands are proposals, not actions to execute.
- Work only from these observations; distinguish demonstrated facts from follow-up hypotheses.
- Show commands as proposed operator actions, not commands you have executed.
- Validate configuration before reload and include an external request check afterward.
- Do not disable security controls or expose the application on all interfaces to solve this mismatch.

# Evaluation criteria

1. Correlates the upstream target with the actual application listener.
2. Distinguishes connection refusal from HTTP application failure and timeouts.
3. Provides a small coherent change with safe validation and rollback.
4. Checks service health from the relevant network locations.
5. Offers evidence-driven follow-up without inventing infrastructure.
