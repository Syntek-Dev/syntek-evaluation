---
benchmark: emails--meeting-summary
version: 2
domain: emails
capability: meeting-action-extraction
jurisdiction: UK
expected_output: email
scoring: qualitative
---
# Task

Turn these fictional meeting notes into a summary email to the existing project
group. Meeting: 14 September 2026, 11:00 BST. Participants: Sam (sponsor), Leah
(delivery), Omar (security), Eva (client operations).

Sam: "Let's aim for a 5 October pilot, provided security signs off."
Leah: "I will send the revised plan by 17 September. The integration estimate
is still between four and seven working days."
Omar: "I can review the access design once Eva sends the role list. I have not
approved the design and cannot commit a review date without that list."
Eva: "I'll send the role list by 16 September. I suggested training on the
morning of 1 October, but I still need to check staff availability."
Sam: "Agreed: pilot only, no production rollout approval today. Leah and I will
review the unresolved dates after the security review."

The rough minutes incorrectly say "5 October launch approved; Omar sign-off
18 September; training booked". Write the accurate email with decisions,
actions and unresolved points distinguished, suitable for participants to correct.

# Constraints

- This is a closed-book benchmark. Use the supplied evidence and rules; do not browse, run commands, or claim external verification. Any requested code or commands are proposals, not actions to execute.
- Use a subject and 180-240-word body; bullets or a compact action table are allowed.
- For unagreed dates write "not agreed" or equivalent instead of inferring them.
- Do not add participants, approvals or owners beyond the notes.

# Evaluation criteria

1. Separates confirmed decisions from provisional targets.
2. Extracts action owners and explicit deadlines correctly.
3. Represents dependency and estimate uncertainty.
4. Corrects the three inaccuracies in the rough minutes.
5. Produces a readable summary with a request for corrections.
