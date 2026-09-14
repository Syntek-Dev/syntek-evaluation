---
benchmark: debugging--git-conflict
version: 2
domain: debugging
capability: merge-conflict-resolution
jurisdiction: UK
expected_output: resolved-code-and-tests
scoring: qualitative
---
# Task

Resolve a fictional Git merge conflict in a Python 3.12 invoice helper. The common ancestor calculated a total with floats. One branch switched to Decimal for currency; the other introduced a loyalty discount. Both changes are required. The approved product contract is: rows are already validated dictionaries with price as a two-decimal string and qty as a positive integer; add all line totals exactly, apply the supplied Decimal discount once to the invoice subtotal, then round to pennies using ROUND_HALF_UP. discount defaults to Decimal('0') and is already validated in [0,1], with at most six fractional digits. Inputs are validated to contain at most 10,000 rows, price at most 999999.99, and qty at most 10,000; the function need not repeat that validation. These bounds make a local Decimal context with precision 28 sufficient for exact intermediate arithmetic. Return Decimal, and do not mutate rows.

    from decimal import Decimal, ROUND_HALF_UP

    <<<<<<< HEAD
    def total(rows):
        return sum((Decimal(r['price']) * r['qty'] for r in rows), Decimal('0')).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    =======
    def total(rows, discount=0):
        return round(sum(float(r['price']) * r['qty'] for r in rows) * (1-discount), 2)
    >>>>>>> loyalty-discount

Supply the resolved function and a small set of tests that would reject choosing either side unchanged. Describe a cautious local sequence to finish the existing merge after reviewing the result. The working tree also contains an unrelated uncommitted README edit that must be preserved.

# Constraints

- This is a closed-book benchmark. Use the supplied evidence and rules; do not browse, run commands, or claim external verification. Any requested code or commands are proposals, not actions to execute.
- Resolve the behaviour from the product contract, not branch-name preference.
- Do not use reset --hard, discard unrelated edits, or assume the entire working tree should be staged.
- You are proposing code and commands only; do not claim a merge or tests were executed.
- Use a local Decimal context with precision 28, independent of caller context, and include the empty-input case.

# Evaluation criteria

1. Combines both intentional changes without retaining conflict markers.
2. Applies discount and rounding at the specified boundary.
3. Covers edge cases that distinguish competing implementations.
4. Proposes inspecting and staging only the resolved file.
5. Preserves unrelated work and describes appropriate verification.
