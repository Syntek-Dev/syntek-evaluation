---
benchmark: hr--disciplinary-scenario
version: 2
domain: hr
capability: fair-investigation
jurisdiction: UK
expected_output: investigation-plan-and-neutral-invitation
scoring: qualitative
---
# Task

A warehouse manager seeks to dismiss Taylor for leaving before a 17:00 shift end on 12 May 2027. Badge data shows an exit at 16:20 local time. CCTV export labels Taylor near the loading bay at 15:35 UTC; the packet stipulates local time was UTC+1. A supervisor text at 16:10 local says “finish the loading job then head off”; the supervisor now says this was addressed to a different worker, but the displayed recipient is Taylor. A colleague reports seeing Taylor leave “around four,” without checking a clock. No payroll loss, safety incident or previous warning is recorded. Synthetic policy says investigations must consider evidence both for and against an allegation, give the worker a meaningful response opportunity, and separate the investigator from the decision maker where practicable. Precautionary suspension requires a documented reason and consideration of alternatives; it is not automatic. Draft a neutral allegation, rank the evidence and its limits, identify preservation and interview steps, and recommend the immediate process without deciding guilt or a sanction.

# Constraints

- This is a closed-book benchmark. Use the supplied evidence and rules; do not browse, run commands, or claim external verification. Any requested code or commands are proposals, not actions to execute.
- Treat quoted policies as synthetic internal benchmark rules, not statements of current UK employment law.
- Provide preliminary people-management analysis for an England and Wales employer; identify specific issues needing qualified HR or legal advice.
- Use observable evidence, maintain proportionate confidentiality, and do not infer motives, diagnoses or protected characteristics beyond stated facts.
- Use the supplied time-zone offset exactly; do not infer that the CCTV or badge identification is correct without verification.

# Evaluation criteria

1. Normalises timestamps and identifies contradictory evidence.
2. Explores the apparent permission message and recipient dispute fairly.
3. Separates fact finding, interim measures and any later sanction decision.
4. Plans proportionate evidence preservation and a meaningful response opportunity.
5. Drafts neutral language without assumptions of dishonesty or misconduct.
