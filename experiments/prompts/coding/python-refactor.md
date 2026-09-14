---
benchmark: coding--python-refactor
version: 2
domain: coding
capability: behaviour-preserving-refactor
jurisdiction: UK
expected_output: analysis-and-code
scoring: qualitative
---
# Task

A fictional UK invoicing service runs CPython 3.12. Refactor this function for clarity and reliable money arithmetic. Input rows come from a JSON request. The public contract is: sku is a nonempty string; qty is an integer greater than zero (booleans do not count); price is a decimal string with at most two fractional digits and must be nonnegative. Missing or invalid fields must raise ValueError identifying the row index. An empty list returns an empty dict. Aggregate repeated SKUs and apply the supplied discount once per SKU; round once, at the end, to pennies using ROUND_HALF_UP. There may be at most 10,000 rows; each price must be at most 999999.99 and each qty at most 10,000. discount is a decimal string in the inclusive range 0 to 1 with at most six fractional digits. Reject inputs outside these bounds. These bounds make an explicit local Decimal context with precision 28 sufficient for every intermediate result. Do not mutate input.

    def totals(rows, discount='0'):
        result = {}
        for r in rows:
            result[r['sku']] = round(result.get(r['sku'], 0) +
                float(r['price']) * r['qty'] * (1-float(discount)), 2)
        return result

Return a complete implementation, three focused examples that distinguish it from the original, and a concise explanation of compatibility changes. Return money values as Decimal objects; no JSON serialization is required.

# Constraints

- This is a closed-book benchmark. Use the supplied evidence and rules; do not browse, run commands, or claim external verification. Any requested code or commands are proposals, not actions to execute.
- Use only the Python 3.12 standard library; work from this specification without external tools.
- Reject NaN, infinity, scientific notation, and excess fractional precision rather than silently normalising them.
- Do not add persistence, networking, or an unrelated validation framework.
- Use a local Decimal context with precision 28, independent of caller context; reject the supplied row-count and numeric bounds before arithmetic.

# Evaluation criteria

1. Preserves grouping and input immutability while implementing the stated monetary contract.
2. Handles malformed rows, quantities, prices, and discount explicitly.
3. Places rounding at the required boundary and uses the requested rounding mode.
4. Provides executable code with clear errors and bounded responsibilities.
5. Uses examples that expose meaningful edge cases rather than only a happy path.
