---
benchmark: security--web-security-review
version: 2
domain: security
capability: browser-security-review
jurisdiction: UK
expected_output: prioritised-review-and-fixes
scoring: qualitative
---
# Task

Review this fictional browser-based account application. It runs at https://portal.example.test and uses a session cookie with Secure, HttpOnly and SameSite=Lax. The server authenticates every account route. Two implementation excerpts and current headers are:

Browser:
    const q = new URLSearchParams(location.search).get('notice') || '';
    document.querySelector('#notice').innerHTML = q;

Server route:
    GET /account/change-email?email=...
    # updates the authenticated account email immediately
    # no CSRF token, no reauthentication, no email confirmation

Headers:
    Content-Security-Policy: default-src 'self'; script-src 'self' 'unsafe-inline'
    Access-Control-Allow-Origin: *
    # Access-Control-Allow-Credentials is not sent

Explain the concrete browser security risks, relevant interaction between cookie settings and the state-changing GET route, and the limits of the CORS evidence. Propose minimal code/route/header changes, then give a defensive verification plan. An operator says HttpOnly makes the innerHTML assignment harmless because scripts cannot read the session cookie. Assess that claim precisely. Do not assume unrelated account routes are vulnerable or that every cross-origin response can be read with credentials.

# Constraints

- This is a closed-book benchmark. Use the supplied evidence and rules; do not browse, run commands, or claim external verification. Any requested code or commands are proposals, not actions to execute.
- Do not construct exploit URLs or execute attacks; describe safe local test cases.
- Keep XSS, CSRF, CORS and authentication concepts distinct.
- Preserve legitimate plain-text notices and the ability to change email through a protected workflow.
- Do not treat a header change as a substitute for fixing unsafe rendering or request semantics.

# Evaluation criteria

1. Identifies the unsafe rendering sink and its impact despite HttpOnly.
2. Explains state-changing GET exposure with SameSite=Lax accurately.
3. Interprets wildcard CORS without inventing credentialed read access.
4. Proposes coherent rendering, CSRF, confirmation and CSP changes.
5. Provides focused verification and appropriately scoped findings.
