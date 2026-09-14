---
benchmark: project-management--risk-register
version: 2
domain: project-management
capability: risk-prioritisation
jurisdiction: UK
expected_output: risk-register
scoring: qualitative
---
# Task

Build a fictional project risk register from these facts. Pilot launch is in
20 working days. The sole database specialist is booked for leave on days 12-16;
restore testing is currently planned for day 14. A supplier's sandbox credentials
were due yesterday and have not arrived. A feature flag allows the supplier
integration to be excluded from the pilot only if the sponsor agrees. Load tests
have reached 40 concurrent users; the requirement is 100 and nobody has tested
above 40. The budget has £8,000 contingency. A second supplier test environment
could cost £3,000, but no quote or compatibility evidence exists. The sponsor
wants numerical probability percentages for every risk despite the lack of data.

Produce five or fewer entries with cause-event-impact statements, owner by role,
likelihood and impact rationale, response, trigger and residual risk. Separate
an issue that has already occurred from uncertain future events. Include two
immediate actions and explain how you would improve estimation without making
up probabilities or treating contingency cash as a complete response.

# Constraints

- This is a closed-book benchmark. Use the supplied evidence and rules; do not browse, run commands, or claim external verification. Any requested code or commands are proposals, not actions to execute.
- Use qualitative likelihood when the packet cannot justify percentages.
- Do not count the late credentials as a merely hypothetical event.
- Treat supplier substitution and scope reduction as decisions requiring evidence/approval.

# Evaluation criteria

1. Separates current issues from future risks.
2. Uses specific cause-event-impact descriptions.
3. Assigns useful owners, triggers and responses.
4. Handles probability, cost and residual uncertainty honestly.
5. Prioritises concrete immediate actions.
