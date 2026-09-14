---
benchmark: emails--sensitive-communication
version: 2
domain: emails
capability: privacy-aware-writing
jurisdiction: UK
expected_output: email-and-private-note
scoring: qualitative
---
# Task

Draft a team email from manager Ellis about a temporary rota change. The team
only needs to know that Jordan will be away from 5 to 16 October inclusive,
Priya will handle urgent customer escalations and Ellis will allocate other work
at the morning check-in. Existing client deadlines remain under review; nobody
has approved overtime. Jordan has agreed to sharing the absence dates and cover
arrangements, but has explicitly asked that the reason remain private.

The manager's private notes say Jordan is receiving treatment for a health
condition and a family member is also unwell. A colleague speculated in a group
chat that the absence was disciplinary. There is no disciplinary process.
Ellis wants to discourage speculation without repeating it or disclosing private
health or family details. The team email must not invite staff to contact Jordan
during the absence. Questions about workload should go to Ellis.

Return the email and a separate short private note stating which details you
excluded and how Ellis should handle requests for more information.

# Constraints

- This is a closed-book benchmark. Use the supplied evidence and rules; do not browse, run commands, or claim external verification. Any requested code or commands are proposals, not actions to execute.
- Email body 90-140 words; private note at most 70 words.
- Keep sensitive reasons and the specific rumour out of the email.
- Do not imply a guaranteed return, overtime requirement or confirmed deadline changes.

# Evaluation criteria

1. Shares only agreed dates and necessary cover arrangements.
2. Protects health, family and disciplinary information.
3. Discourages speculation without amplifying it.
4. Directs workload questions appropriately and respects leave.
5. Separates private rationale from the sendable email.
