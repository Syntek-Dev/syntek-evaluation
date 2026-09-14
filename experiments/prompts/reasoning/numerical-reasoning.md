---
benchmark: reasoning--numerical-reasoning
version: 2
domain: reasoning
capability: inventory-and-money-arithmetic
jurisdiction: UK
expected_output: worked-calculation
scoring: qualitative
---
# Task

A fictional warehouse closes its weekly stock ledger. It starts with 1,200 saleable units and zero quarantined units. During the week it receives 380 new saleable units, accepts 50 customer-returned units of which 40 pass inspection and 10 remain quarantined, ships 975 saleable units, and scraps 25 saleable units. These movements are disjoint and complete; no shipped or scrapped units are counted twice.

The replenishment policy triggers an order if closing saleable stock is below 700 units. It orders the smallest whole number of packs of 24 that would bring saleable stock to at least 1,100 units when delivered. The supplier charges GBP 7.50 per unit before an 8% discount on merchandise only. Freight is GBP 60 per order. For this fictional invoice, exactly 20% tax is applied to discounted merchandise plus freight. The order arrives in full immediately after closing, with no intervening movements. Quarantined units do not count toward either threshold.

Calculate closing saleable and quarantined stock, whether an order is triggered, pack count and unit count, discounted merchandise cost, taxable subtotal, tax, total invoice, and saleable stock after delivery. Show equations that make each stage auditable and distinguish stock quantities from currency.

# Constraints

- This is a closed-book benchmark. Use the supplied evidence and rules; do not browse, run commands, or claim external verification. Any requested code or commands are proposals, not actions to execute.
- Use the supplied fictional invoice rules; do not introduce external tax or accounting rules.
- Use exact decimal money calculations and show final currency values to two decimal places.
- Apply the discount before freight and tax, with no discount on freight.
- Keep quarantined units separate throughout the replenishment calculation.

# Evaluation criteria

1. Reconciles every inventory movement without omission or double counting.
2. Applies the trigger and pack-rounding policy correctly.
3. Calculates discount, freight, and tax in the prescribed order.
4. Shows traceable equations with clear units and precision.
5. Cross-checks the final stock level against the target and pack constraint.
