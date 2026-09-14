---
benchmark: security--authentication-design
version: 2
domain: security
capability: authentication-and-recovery-design
jurisdiction: UK
expected_output: authentication-design-and-abuse-cases
scoring: qualitative
---
# Task

Design authentication for a fictional UK internal application used by 300 employees. A trusted corporate identity provider already supports OIDC authorization code flow and phishing-resistant MFA. The application is a browser frontend with a server-side backend; it need not store employee passwords. Administrators can approve payment batches, so those actions require recent strong authentication. The identity provider can disable an account and send a signed lifecycle event; the application must stop that user accessing protected data within 60 seconds. Sessions should survive ordinary page refreshes. A proposal puts an access token in localStorage, issues a 30-day application session with no server record, and treats possession of a recovery email link as sufficient for administrator access.

Evaluate the proposal and design sign-in, session storage, renewal, logout, account-disable propagation and administrator recovery. Include protection against login CSRF/session fixation, browser token exposure, replay and enumeration. State how recent strong authentication is established for sensitive actions and what happens if the identity provider is unavailable. Describe evidence and audit events without recording tokens or authorization codes. Do not make assumptions about an identity-provider feature beyond the capabilities explicitly supplied.

# Constraints

- This is a closed-book benchmark. Use the supplied evidence and rules; do not browse, run commands, or claim external verification. Any requested code or commands are proposals, not actions to execute.
- Use the existing identity provider rather than inventing a password database or cryptographic protocol.
- Do not promise 60-second revocation with indefinitely trusted offline sessions.
- Separate routine employee recovery from restoration of privileged approval rights.
- Discuss external-provider outage behaviour and preserve the recent-authentication requirement.

# Evaluation criteria

1. Uses an appropriate browser/backend sign-in flow with verified identity assertions.
2. Provides secure session handling and fixation/CSRF defenses.
3. Meets the disable-propagation bound across sessions and caches.
4. Protects sensitive-action reauthentication and privileged recovery.
5. States outage behaviour, audit needs and residual assumptions clearly.
