---
benchmark: security--threat-model
version: 2
domain: security
capability: bounded-threat-modelling
jurisdiction: UK
expected_output: threat-model-and-priorities
scoring: qualitative
---
# Task

Threat-model a fictional multi-tenant document conversion service. Authenticated customers upload PDFs or supply an HTTPS URL. An API records the tenant and job in PostgreSQL 16. A worker fetches URL content, converts it using a native parser, and writes an output object. The worker currently shares a host and network namespace with a local model server and an instance metadata endpoint. The API returns a download URL. A support dashboard shows job names and parser error text. Customers must never read another tenant document. Uploaded files and fetched responses are untrusted, even if a customer account is paid. The parser occasionally crashes on malformed files; no exploit has been demonstrated.

Identify assets, actors, entry points and trust boundaries, then prioritise five concrete abuse cases. For each, state the attacker precondition, plausible impact, preventive/detective controls and a residual risk or verification need. Include the URL-fetch path, parser isolation, tenant authorization, browser rendering of support diagnostics and resource exhaustion. End with the first three engineering changes you would fund for a two-week hardening sprint, explaining the ordering. Distinguish a credible exploit path from a confirmed incident.

# Constraints

- This is a closed-book benchmark. Use the supplied evidence and rules; do not browse, run commands, or claim external verification. Any requested code or commands are proposals, not actions to execute.
- Do not provide attack payloads or perform testing; describe defensive checks and bounded test objectives.
- Do not treat TLS, paid accounts or file extensions as proof that content is safe.
- Use the supplied architecture; clearly label any assumptions about access rights or parser behaviour.
- Prioritise controls against actual boundaries rather than listing unrelated security products.

# Evaluation criteria

1. Maps specific assets and trust boundaries in the supplied system.
2. Explains five distinct threats with preconditions and plausible impact.
3. Pairs threats with preventative, detective and verification measures.
4. Prioritises a feasible sprint with reasons and residual risks.
5. Avoids claiming an exploit or incident from crash evidence alone.
