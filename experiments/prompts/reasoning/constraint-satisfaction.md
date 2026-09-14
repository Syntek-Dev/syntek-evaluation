---
benchmark: reasoning--constraint-satisfaction
version: 2
domain: reasoning
capability: unique-assignment-solving
jurisdiction: UK
expected_output: assignment-and-proof
scoring: qualitative
---
# Task

A fictional support team must assign four people, Asha (A), Ben (B), Chen (C), and Dev (D), to four chronological half-day slots. The slots, indexed 1 through 4, are Tuesday morning, Tuesday afternoon, Wednesday morning, and Wednesday afternoon. Exactly one person covers each slot and each person covers exactly one slot.

All scheduling rules are listed here:
- Asha cannot work on Tuesday.
- Ben can work only in an afternoon slot.
- Chen can work only in a morning slot.
- Chen's slot must occur earlier than Dev's slot.
- Ben's slot must immediately follow Asha's slot in the four-slot sequence; no slot can intervene.

There are no skill restrictions, preferences, travel limits, or other availability constraints. A coordinator proposes the chronological assignment Chen, Asha, Dev, Ben. Treat that proposal as a candidate to evaluate, not as a new requirement.

Find every valid assignment under the rules and state whether the solution is unique. Explain your eliminations so a reader can check completeness without trusting a black-box solver. Evaluate the coordinator's proposal against each relevant rule and identify all violations. Finally, explain whether removing the rule that Chen works before Dev would produce additional solutions, keeping all other rules unchanged.

# Constraints

- This is a closed-book benchmark. Use the supplied evidence and rules; do not browse, run commands, or claim external verification. Any requested code or commands are proposals, not actions to execute.
- Use the exact chronological slot sequence; immediately follows is not merely later in the week.
- Enforce the one-person-per-slot and one-slot-per-person conditions.
- Do not invent preferences to resolve a tie.
- Check the altered-rule question independently and enumerate any alternatives.

# Evaluation criteria

1. Translates availability and ordering rules accurately.
2. Produces all feasible assignments and supports completeness.
3. Distinguishes uniqueness from finding a single example.
4. Identifies every violation in the proposed schedule.
5. Assesses the rule-removal variant without carrying over unsupported assumptions.
