---
benchmark: research--comparative-research
version: 2
domain: research
capability: comparative-evaluation
jurisdiction: UK
expected_output: requirements-matrix-and-pilot-plan
scoring: qualitative
---
# Task

Choose a candidate search service for a UK archive using this synthetic packet. Required conditions are no document-content egress outside the UK, support for scanned PDFs, a documented deletion process covering active storage and backups with completion deadlines and p95 query latency under two seconds on the archive's workload. S-A is Alpha's signed specification: UK processing, scanned-PDF OCR, deletion from active storage within 24 hours and backups within 30 days. Alpha's benchmark reports p95 1.4 seconds on 1,000 short text PDFs; it reports no OCR workload test. S-B is Beta's specification: p95 0.9 seconds on 500 scanned PDFs, OCR included, processing in UK or EU “as capacity requires,” and deletion “on request” with no completion deadline. S-C is Gamma's independent pilot note: p95 1.8 seconds on 100 scanned PDFs from another archive, UK processing confirmed for that pilot, but deletion documentation unavailable. Cost data and contractual location guarantees for Gamma are missing. Create a requirement-by-vendor matrix using met, failed or unverified with source citations, recommend the next procurement step and specify an acceptance pilot.

# Constraints

- This is a closed-book benchmark. Use the supplied evidence and rules; do not browse, run commands, or claim external verification. Any requested code or commands are proposals, not actions to execute.
- Use only the labelled synthetic source packet; all organisations and study details are fictional benchmark inputs.
- Cite evidence with the supplied source IDs. Do not browse, fabricate real citations or imply that missing evidence has been checked.
- Separate direct observations, calculations, interpretations and unresolved questions; avoid unsupported causal or certainty claims.
- Do not equate a different-corpus benchmark or one pilot deployment with a binding production guarantee.

# Evaluation criteria

1. Evaluates all mandatory requirements separately using traceable evidence.
2. Distinguishes explicit failures from missing verification.
3. Recognises that benchmark corpus and deployment conditions affect comparability.
4. Avoids claiming any vendor meets all requirements without evidence.
5. Designs measurable acceptance checks and prioritises missing commercial information.
