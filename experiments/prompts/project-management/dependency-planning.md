---
benchmark: project-management--dependency-planning
version: 2
domain: project-management
capability: dependency-resolution
jurisdiction: UK
expected_output: dependency-plan
scoring: qualitative
---
# Task

You inherit this fictional release checklist. A contract signature is required
before B production credentials. B is required before C live smoke test. C is
required before D customer acceptance. D is required before A contract signature.
Legal owner of A says the draft mistakenly uses "acceptance" for both a sandbox
design review and final live acceptance; they have not yet approved a correction.
Sandbox credentials and synthetic test data already exist, so a separate sandbox
review is technically possible without A or B. The production credential owner
cannot waive the signed-contract requirement. The final live acceptance cannot
be simulated or skipped.

An executive asks the team to "just run the checklist in the right order" by
Friday. Identify the dependency problem, distinguish a logical blocker from an
estimated duration risk, and propose a corrected dependency model conditional
on the relevant owner's approval. Include a clear decision request, interim work
that can proceed now, and the evidence needed before claiming a release date.
Use a compact edge list or diagram plus a short explanation.

# Constraints

- This is a closed-book benchmark. Use the supplied evidence and rules; do not browse, run commands, or claim external verification. Any requested code or commands are proposals, not actions to execute.
- Treat the stated dependencies as binding until their owner approves a change.
- Do not use real production credentials without a signed contract.
- Do not infer task durations or guarantee Friday.

# Evaluation criteria

1. Identifies the dependency cycle accurately.
2. Explains why ordering alone cannot solve it.
3. Proposes a valid, explicitly conditional dependency change.
4. Separates safe interim work from blocked production steps.
5. Names the approval and scheduling evidence needed.
