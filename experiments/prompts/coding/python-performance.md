---
benchmark: coding--python-performance
version: 2
domain: coding
capability: algorithmic-performance
jurisdiction: UK
expected_output: analysis-and-code
scoring: qualitative
---
# Task

A fictional CPython 3.12 batch job has 2,000,000 events and 50,000 account records. It currently runs the code below. Events have account_id: str and amount_pence: int. Accounts have id: str and region: str. Account records are ordered by ingestion time; if an id appears more than once, the last record is authoritative. Events whose account is absent must be counted as unmatched and excluded from region totals. Return region totals ordered by the first included event seen for that region, plus the unmatched count.

    def summarise(events, accounts):
        totals = {}
        for event in events:
            for account in accounts:
                if event['account_id'] == account['id']:
                    region = account['region']
                    totals[region] = totals.get(region, 0) + event['amount_pence']
        return totals

Propose and implement an improvement suitable for a one-pass event iterator. Account records fit in memory. Explain time and auxiliary-space complexity, distinguish algorithmic gains from unmeasured runtime claims, and show a small example including a duplicate account, a negative amount, and an unmatched event.

# Constraints

- This is a closed-book benchmark. Use the supplied evidence and rules; do not browse, run commands, or claim external verification. Any requested code or commands are proposals, not actions to execute.
- Use the Python 3.12 standard library and integer pence; no database or dataframe dependency.
- Do not materialise the event iterator or change the stated duplicate-account rule.
- Treat inputs as already schema-validated and do not mutate them.

# Evaluation criteria

1. Identifies both complexity and correctness problems in the original loop.
2. Implements the required account precedence and unmatched-event handling.
3. Processes events in one pass with predictable auxiliary memory.
4. Preserves required output order and signed integer arithmetic.
5. Provides accurate complexity reasoning and a discriminating example.
