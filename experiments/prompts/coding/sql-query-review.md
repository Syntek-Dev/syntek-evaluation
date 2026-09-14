---
benchmark: coding--sql-query-review
version: 2
domain: coding
capability: sql-correctness
jurisdiction: UK
expected_output: analysis-and-sql
scoring: qualitative
---
# Task

A fictional PostgreSQL 16 database has customers(id, name), orders(id, customer_id, total_pence, status), and refunds(id, order_id, amount_pence). A paid order can have multiple refund rows. Report every customer, the count of their paid orders, and net_pence = paid order totals minus refunds attached to those paid orders. Customers without paid orders must receive zeros. All amounts are integer pence and all foreign keys are valid.

    SELECT c.id, count(o.id) AS paid_orders,
           sum(o.total_pence)-sum(r.amount_pence) AS net_pence
    FROM customers c
    LEFT JOIN orders o ON o.customer_id=c.id
    LEFT JOIN refunds r ON r.order_id=o.id
    WHERE o.status='paid'
    GROUP BY c.id;

Data: customers (1,'A'), (2,'B'), (3,'C'); orders (10,1,10000,'paid'), (11,1,3000,'draft'), (12,3,5000,'paid'); refunds (100,10,1000), (101,10,500). Diagnose the query, give a corrected query and the exact expected rows ordered by customer id. Explain any indexes you would investigate for a much larger dataset and what evidence you need before asserting a speed improvement.

# Constraints

- This is a closed-book benchmark. Use the supplied evidence and rules; do not browse, run commands, or claim external verification. Any requested code or commands are proposals, not actions to execute.
- Do not alter the schema, discard repeated refund rows, or use floating-point currency.
- Use PostgreSQL 16 SQL; work from the supplied rows without executing queries.
- Keep correctness reasoning separate from unmeasured performance claims.

# Evaluation criteria

1. Recognises join multiplication and null aggregate behaviour.
2. Retains customers without paid orders while filtering eligible orders.
3. Computes order counts and money without double counting.
4. Derives exact expected results from the fixture.
5. Recommends proportionate performance investigation grounded in access patterns.
