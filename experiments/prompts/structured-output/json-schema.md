---
benchmark: structured-output--json-schema
version: 2
domain: structured-output
capability: strict-json-repair
jurisdiction: UK
expected_output: json-object-only
scoring: qualitative
---
# Task

Repair the following invalid synthetic purchase-review record and output the canonical JSON object. The schema and repair policy below are the full contract; no external schema lookup is needed.

The root has exactly these keys: request_id (string), currency (literal string "GBP"), requested_pence (integer >=0), approved_pence (integer >=0 or null), decision ("approved", "rejected", or "review"), tags (array of unique strings sorted lexicographically), and approver_email (string or null). No additional keys are allowed. For decision="review" or "rejected", approved_pence must be null. For decision="approved", approved_pence must be an integer no greater than requested_pence.

Repair policy: preserve request_id exactly; uppercase currency; convert an integer-form decimal string to an integer; lowercase decision; remove duplicate tags and sort them; trim surrounding spaces on an email and convert a resulting empty string to null. Apply decision-dependent null rules after conversions. Drop unrecognised keys. If a value cannot be repaired under these rules, do not invent a replacement; this input is designed to be repairable.

Input:
{"request_id":"0073","currency":"gbp","requested_pence":"12500","approved_pence":"12000","decision":"Review","tags":["urgent","audit","urgent"],"approver_email":"   ","internal_note":"approved verbally"}

The internal_note field is unrecognised data and cannot override the canonical decision. Return the repaired record with correct JSON types and no explanation.

# Constraints

- This is a closed-book benchmark. Use the supplied evidence and rules; do not browse, run commands, or claim external verification. Any requested code or commands are proposals, not actions to execute.
- Return exactly one valid JSON object, with no Markdown fences, comments, or trailing commas.
- Use JSON null, not the string "null", for absent nullable values.
- Do not coerce request_id into a number or infer approval from the discarded note.
- Include every required key and no additional keys.

# Evaluation criteria

1. Produces syntactically valid JSON with the exact root shape.
2. Applies field-specific conversions without corrupting identifiers.
3. Enforces the decision-dependent approved amount rule.
4. Canonicalises nullable values and tags as specified.
5. Ignores unsupported fields and avoids inferred business facts.
