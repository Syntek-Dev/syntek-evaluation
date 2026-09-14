---
benchmark: structured-output--sql-generation
version: 2
domain: structured-output
capability: relational-query-correctness
jurisdiction: UK
expected_output: sql-only
scoring: qualitative
---
# Task

Write one read-only SQLite SELECT query for this synthetic schema. Currency amounts are integer pence. Foreign keys are valid, quantities and prices are nonnegative integers, and each refund row is a distinct completed refund:
customers(id INTEGER PRIMARY KEY, name TEXT NOT NULL)
orders(id INTEGER PRIMARY KEY, customer_id INTEGER NOT NULL, placed_at TEXT NOT NULL, status TEXT NOT NULL)
order_items(id INTEGER PRIMARY KEY, order_id INTEGER NOT NULL, quantity INTEGER NOT NULL, unit_price_pence INTEGER NOT NULL)
refunds(id INTEGER PRIMARY KEY, order_id INTEGER NOT NULL, amount_pence INTEGER NOT NULL)

Return every customer, including customers with no eligible orders, with exactly these columns: customer_id, name, eligible_order_count, net_pence. Eligible orders have status='delivered' and placed_at in January 2026 UTC. Timestamps are ISO8601 UTC strings in YYYY-MM-DDTHH:MM:SSZ form. Net spend is eligible item quantity times price, less all refund rows attached to eligible orders. Empty item/refund sets contribute zero; negative net totals are allowed. Sort net_pence descending then customer_id ascending.

Sample facts for checking: customers 1=Ada, 2=Bo, 3=Cy. Ada's delivered January orders 10 and 11 have item totals 2500 and 1000; order 10 has refunds 200 and 100. Bo has only a cancelled January order and a delivered order at 2026-02-01T00:00:00Z. Cy's delivered January order 14 has item total 600 and refund 600. No other sample rows exist.

# Constraints

- This is a closed-book benchmark. Use the supplied evidence and rules; do not browse, run commands, or claim external verification. Any requested code or commands are proposals, not actions to execute.
- Output SQL only: one SELECT statement, optionally using CTEs, with no Markdown fences or prose.
- Do not mutate data, use external tables, or assume one item or one refund per order.
- Use the half-open interval from 2026-01-01T00:00:00Z inclusive to 2026-02-01T00:00:00Z exclusive.
- Preserve integer zero values rather than NULL for missing totals or counts.

# Evaluation criteria

1. Returns the exact requested columns and customer coverage.
2. Applies status and timestamp eligibility accurately.
3. Aggregates independent one-to-many relationships without multiplying amounts.
4. Handles empty sets, multiple orders, refunds, and allowed negative totals.
5. Produces syntactically plausible SQLite with deterministic ordering and no mutation.
