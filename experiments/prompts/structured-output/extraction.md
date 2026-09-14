---
benchmark: structured-output--extraction
version: 2
domain: structured-output
capability: source-precedence-extraction
jurisdiction: UK
expected_output: json-object-only
scoring: qualitative
---
# Task

Extract a canonical quote from these synthetic messages. Newer explicit corrections override older values only for fields they name. Relative date phrases are not converted to calendar dates under this extraction policy, even when a message timestamp is present. No contact email is supplied; do not invent one from a company name.

Message 1, 2026-09-09T10:00:00Z:
Vendor: Marlow Components Ltd. Quote Q-17. Currency GBP. Line SKU-BOLT: quantity 10, unit price GBP 1.25. Line SKU-SEAL: quantity 4, unit price GBP 2.40. Delivery: next Friday. Please reply to the sales team through the portal.

Message 2, 2026-09-10T11:30:00Z:
Correction to Q-17: SKU-BOLT quantity is 12. All other quote values remain unchanged. Delivery is still next Friday. Please retain Q-17, including its hyphen, as the quote identifier.

Return exactly one object with keys vendor(string), quote_id(string), currency(string), items(array), merchandise_total_pence(integer), delivery_date(string in YYYY-MM-DD form or null), contact_email(string or null), warnings(array of strings). Each item has exactly sku(string), quantity(integer), and unit_price_pence(integer). Sort items lexicographically by sku. The only warning codes permitted here are MISSING_CONTACT_EMAIL and RELATIVE_DELIVERY_DATE; include every applicable code once and sort lexicographically. Convert prices to integer pence without floating-point artefacts. Do not include tax or shipping because neither is specified.

# Constraints

- This is a closed-book benchmark. Use the supplied evidence and rules; do not browse, run commands, or claim external verification. Any requested code or commands are proposals, not actions to execute.
- Output valid JSON only, with exactly the required keys and no Markdown fences.
- Preserve identifiers and vendor spelling from the messages.
- Represent unknown nullable fields with JSON null and include the required warning codes.
- Apply explicit field corrections without discarding unchanged lines or inventing unstated charges.

# Evaluation criteria

1. Extracts source values and applies message precedence correctly.
2. Converts quantities and money into the required JSON types.
3. Computes the merchandise total from the corrected line items.
4. Handles unspecified and relative values according to the null policy.
5. Produces the exact schema, deterministic ordering, and applicable warning codes.
