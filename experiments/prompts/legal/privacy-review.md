---
benchmark: legal--privacy-review
version: 2
domain: legal
capability: privacy-notice-review
jurisdiction: UK
expected_output: gap-table-and-revised-notice
scoring: qualitative
---
# Task

Review a proposed privacy notice for an England and Wales appointment service. Draft: “We collect only anonymous information to improve your experience. We never share data. Everything is deleted after 30 days. By using the service you agree to all future changes.” The supplied data inventory says booking records contain name, email, appointment reason and account ID; appointment reasons sometimes mention medical conditions. Email delivery provider PostRelay receives email addresses and message bodies. Support staff can search bookings for 12 months; encrypted backups expire after 90 days. Product analytics receives account IDs and event times; the service maintains the lookup from IDs to people. For this synthetic exercise, a notice must describe identifiable data categories, distinct purposes, recipient categories, actual retention practices and a contact route for requests. That requirement alone does not establish a lawful basis or authorise any processing. Deliver a line-by-line gap table, a concise replacement notice with visible placeholders for unresolved details, and a list of engineering or governance changes that cannot be fixed by wording alone.

# Constraints

- This is a closed-book benchmark. Use the supplied evidence and rules; do not browse, run commands, or claim external verification. Any requested code or commands are proposals, not actions to execute.
- Treat all quoted provisions and interpretation rules as synthetic benchmark inputs, not statements of current UK law.
- Give preliminary analysis for an England and Wales business; distinguish contractual interpretation from questions requiring a qualified solicitor.
- Use only the supplied facts. Identify missing information instead of inventing legal authorities or commercial agreements.
- Do not claim that encryption, pseudonyms, a notice or continued use automatically establishes compliance or consent.

# Evaluation criteria

1. Tests each promise against the inventory and identifies material contradictions.
2. Distinguishes pseudonymisation from anonymous data in this scenario.
3. Explains live-system and backup retention accurately without overpromising.
4. Drafts clear notice text with explicit unresolved fields.
5. Separates communication corrections from operational and legal decisions.
