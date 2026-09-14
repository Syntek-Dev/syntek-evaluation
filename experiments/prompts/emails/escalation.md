---
benchmark: emails--escalation
version: 2
domain: emails
capability: decision-escalation
jurisdiction: UK
expected_output: email
scoring: qualitative
---
# Task

You are delivery lead Asha. Write an internal escalation to sponsor Chris on
Tuesday 22 September 2026 at 09:00 BST. Production acceptance testing was due to
start today and requires client test accounts. Requests were sent on 15 and
18 September; client contact Ben replied on 18 September that approval was
pending. No accounts have arrived. The team has completed the available offline
tests. The release target is 29 September and needs four full working days of
acceptance testing plus one working day of review, in sequence. Wednesday
23 September is the earliest testing can now start. Weekdays only; no holidays.
Release may start only at the beginning of the next working day after review
has completed.

The client has not authorised shortened testing or weekend access. Asha can
reassign two engineers to documentation for one day. Chris can seek an access
decision or agree a revised date with the client, but cannot approve the client's
accounts. Ask Chris for a specific intervention by 12:00 today, explain the
schedule consequence, and give sensible options without blaming Ben.

# Constraints

- This is a closed-book benchmark. Use the supplied evidence and rules; do not browse, run commands, or claim external verification. Any requested code or commands are proposals, not actions to execute.
- Subject and 150-210-word body; treat the release as following completed review.
- Do not invent unapproved overtime or reduce required testing.
- Use factual chronology and distinguish target risk from certainty.

# Evaluation criteria

1. States the blocker, evidence and responsible decision clearly.
2. Calculates the earliest testing/review sequence using weekdays.
3. Connects the delay to release feasibility.
4. Offers practical options within authority.
5. Makes a time-bound escalation request without blame.
