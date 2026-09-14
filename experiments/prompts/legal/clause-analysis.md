---
benchmark: legal--clause-analysis
version: 2
domain: legal
capability: clause-interpretation
jurisdiction: UK
expected_output: worked-analysis-and-revised-clause
scoring: qualitative
---
# Task

Analyse this synthetic delay-damages clause for an England and Wales equipment buyer: “For every calendar day after the contractual delivery date until delivery, Seller shall pay £500, capped at 10% of the £80,000 contract price. Days caused solely by Buyer shall be excluded. These damages are the exclusive remedy for delay, without affecting termination for material breach.” Delivery was due 1 March 2027 and occurred 19 March. For counting, the parties expressly agree there are 18 late calendar days. Site-access records show four of those days were caused solely by Buyer; on another three days both parties had independent causes of delay. Seller argues all seven days must be excluded. Buyer seeks £9,000 plus lost production and asks whether it may terminate automatically. No definition of material breach or other termination clause is supplied. Give both parties' strongest textual arguments, calculate the amount under the wording as supplied, identify unresolved legal and factual issues, and propose a clearer replacement clause that preserves a proportionate commercial remedy.

# Constraints

- This is a closed-book benchmark. Use the supplied evidence and rules; do not browse, run commands, or claim external verification. Any requested code or commands are proposals, not actions to execute.
- Treat all quoted provisions and interpretation rules as synthetic benchmark inputs, not statements of current UK law.
- Give preliminary analysis for an England and Wales business; distinguish contractual interpretation from questions requiring a qualified solicitor.
- Use only the supplied facts. Identify missing information instead of inventing legal authorities or commercial agreements.
- Use the stipulated 18-day count; do not introduce external deadline-counting or enforceability rules.

# Evaluation criteria

1. Interprets solely and concurrent causation using the actual language.
2. Shows the daily calculation and applies the cap in the correct order.
3. Distinguishes delay damages, additional losses and termination rights.
4. Avoids unsupported conclusions about enforceability or material breach.
5. Produces a revision that clarifies causation, counting, caps and remedy interaction.
