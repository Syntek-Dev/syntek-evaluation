---
benchmark: architecture--design-model-router
version: 2
domain: architecture
capability: policy-aware-model-routing
jurisdiction: UK
expected_output: routing-policy-and-decisions
scoring: qualitative
---
# Task

Design a model router from this fictional, frozen evaluation table. Scores are percentages on task-specific held-out fixtures; latency is measured p95 for the fixture workload, and cost is pence per request. A dash means capability was not evaluated.

Model | Location | Code score | Summary score | Policy-analysis score | p95 seconds | Cost pence
Local-S | local | 86 | 95 | 70 | 0.7 | 0.2
Local-L | local | 94 | 93 | 86 | 1.8 | 0.8
Remote-R | external | 96 | 97 | 93 | 1.2 | 2.0

Request A: public summary, minimum score 94, latency budget 1.0 s.
Request B: confidential code, minimum score 90, latency budget 2.0 s.
Request C: confidential policy analysis, minimum score 90, latency budget 2.0 s.
Request D: public policy analysis, minimum score 90, latency budget 2.0 s.

Confidential requests must stay local. Among eligible models choose the lowest supplied cost; no model may be selected if it fails any requirement. State a decision for each request, including an explicit outcome when no model qualifies. Then design a production policy around this simplified exercise: explain why aggregate benchmark scores and p95 figures do not guarantee individual-request quality or deadlines, what to record for audit, and how to validate a routing change before broad rollout.

# Constraints

- This is a closed-book benchmark. Use the supplied evidence and rules; do not browse, run commands, or claim external verification. Any requested code or commands are proposals, not actions to execute.
- Use only the frozen table; do not attach these scores to real products or assume unlisted capabilities.
- Do not lower quality requirements or relabel confidential data to force a selection.
- Keep routing cost arithmetic separate from total infrastructure-cost assumptions.
- Include a safe no-eligible-model path and avoid claiming confidence from an unspecified sample size.

# Evaluation criteria

1. Applies privacy, task score, latency, and cost rules consistently.
2. Makes an explicit justified decision for every supplied request.
3. Recognises the limits of aggregate measurements and missing evaluation context.
4. Provides auditable policy/versioning and controlled rollout.
5. Handles unmet requirements without silent policy bypass.
