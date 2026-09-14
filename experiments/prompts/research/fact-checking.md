---
benchmark: research--fact-checking
version: 2
domain: research
capability: claim-verification
jurisdiction: UK
expected_output: claim-verdict-table-and-corrected-paragraph
scoring: qualitative
---
# Task

Fact-check a draft report against only this synthetic packet. Draft: “Northmere installed 1,000 public chargers in 2026, doubling its network. Its chargers were available 99% of the year, every neighbourhood now has coverage, and the independent audit proves the programme caused a 20% fall in emissions.” S1, a signed asset register dated 31 December 2026, lists 600 operational public charging points, up from 400 a year earlier; 1,000 is the cumulative number of connectors ordered, including replacements and undelivered units. S2, the operator dashboard, reports 99% successful sessions among sessions that started during October–December; it excludes failed starts and provides no annual uptime figure. S3, an internal map, shows operational points in 17 of 20 neighbourhoods. S4, a supplier-funded evaluation, reports a 20% decline in modelled transport emissions since 2024, alongside a new bus service and revised traffic-count methodology; it includes no causal identification design. Return one verdict per separable claim using supported, contradicted or not established, cite IDs and provide a corrected paragraph retaining only defensible statements.

# Constraints

- This is a closed-book benchmark. Use the supplied evidence and rules; do not browse, run commands, or claim external verification. Any requested code or commands are proposals, not actions to execute.
- Use only the labelled synthetic source packet; all organisations and study details are fictional benchmark inputs.
- Cite evidence with the supplied source IDs. Do not browse, fabricate real citations or imply that missing evidence has been checked.
- Separate direct observations, calculations, interpretations and unresolved questions; avoid unsupported causal or certainty claims.
- Do not collapse connectors ordered, operational points, sessions and time-based availability into the same measure.

# Evaluation criteria

1. Splits compound claims into independently assessable statements.
2. Uses correct quantities, dates and metric definitions for each verdict.
3. Distinguishes direct contradiction from lack of evidence.
4. Identifies funding, methodological change and causal-attribution limitations.
5. Rewrites the paragraph faithfully without adding unsupported external facts.
