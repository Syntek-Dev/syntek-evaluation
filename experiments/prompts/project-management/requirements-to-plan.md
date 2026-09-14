---
benchmark: project-management--requirements-to-plan
version: 2
domain: project-management
capability: requirements-decomposition
jurisdiction: UK
expected_output: delivery-plan
scoring: qualitative
---
# Task

Turn these fictional stakeholder requests into a reviewable pilot plan. Sales:
"Upload any document and answer instantly." Security: "Only approved PDF manuals,
at most 20 MB each; no tenant may see another tenant's material." Operations:
"During the pilot, every answer needs a source page and a human can remove a
manual." Sponsor: "Deliver a pilot in four weeks with two engineers; £12,000
is the maximum additional cash spend." Product: "Include scanned documents,
spreadsheet calculations, and voice input if there is time." No OCR component,
latency target, throughput baseline or accessibility acceptance test is selected.
The pilot has 10 named users in two test tenants, using non-sensitive manuals.
No production access or legal compliance certification has been approved.

Provide a requirements table with priorities and testable acceptance criteria,
a four-week delivery outline, unresolved decisions with proposed owners, and
explicit scope boundaries. Resolve conflicts visibly rather than quietly picking
the easiest statement. Explain which estimates and acceptance thresholds must
be agreed before the sponsor can rely on the plan.

# Constraints

- This is a closed-book benchmark. Use the supplied evidence and rules; do not browse, run commands, or claim external verification. Any requested code or commands are proposals, not actions to execute.
- Do not convert "instantly" or "any document" into an unsupported guarantee.
- Preserve tenant isolation and approved-file restrictions as mandatory gates.
- Treat OCR, spreadsheets and voice as unapproved scope, with proposed decisions.

# Evaluation criteria

1. Translates vague requests into testable, scoped requirements.
2. Identifies and resolves conflicts through explicit decisions.
3. Sequences delivery and validation within stated capacity.
4. Defines meaningful isolation, source and deletion acceptance tests.
5. Makes uncertainty, costs and scope boundaries visible.
