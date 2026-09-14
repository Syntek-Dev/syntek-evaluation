---
benchmark: structured-output--decision-record
version: 2
domain: structured-output
capability: constrained-architecture-decision
jurisdiction: UK
expected_output: json-object-only
scoring: qualitative
---
# Task

Create a machine-readable proposed architecture decision for a fictional shared session store. The requirements are C1: all application instances observe the same committed session state; C2: measured p99 lookup latency must be at most 30 ms at the stated test load; C3: incremental monthly cost must be at most GBP80. All three are mandatory. The observations below are exact fixture facts, not claims about these technologies in general:

E1: IN_PROCESS costs GBP10/month and measured p99 is 2 ms, but instances keep separate state and do not share commits.
E2: REDIS costs GBP90/month, measured p99 is 12 ms, and every instance reads the same shared committed state.
E3: POSTGRES costs GBP60/month, measured p99 is 20 ms, and every instance reads the same shared committed state.
E4: These measurements used 100 concurrent sessions; peak production concurrency and failover behavior have not been tested.

Output one JSON object with exactly decision_id(string literal ADR-007), status(string literal proposed), selected(string: IN_PROCESS,REDIS,POSTGRES,or null), assessments(array), and follow_up_codes(array). Assessments must appear in E1,E2,E3 option order. Each assessment has exactly option(string), eligible(boolean), violated_constraints(array of C1/C2/C3 sorted lexicographically), and evidence_ids(array containing that option's observation ID). Follow-up codes must be exactly the applicable values from PEAK_LOAD_TEST and FAILOVER_TEST, sorted lexicographically. Select the sole eligible option if exactly one exists; otherwise selected is null.

# Constraints

- This is a closed-book benchmark. Use the supplied evidence and rules; do not browse, run commands, or claim external verification. Any requested code or commands are proposals, not actions to execute.
- Return valid JSON only, with all required keys and no narrative or Markdown fences.
- Use the supplied measurements and costs without substituting general technology expectations.
- Treat all three constraints as mandatory and preserve proposed status.
- Do not claim E4 gaps are already validated or add unstated eligibility constraints.

# Evaluation criteria

1. Applies each mandatory constraint to every option accurately.
2. Selects an option according to the exact eligibility rule.
3. Connects assessments to the supplied observation identifiers.
4. Records unresolved validation work without overstating readiness.
5. Produces the exact ordered schema with correct Boolean and nullable types.
