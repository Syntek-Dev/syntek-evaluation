---
benchmark: reasoning--dependency-resolution
version: 2
domain: reasoning
capability: finite-version-resolution
jurisdiction: UK
expected_output: version-plan-and-proof
scoring: qualitative
---
# Task

A fictional application installs exactly one version of each of four components: Platform P, plug-in A, plug-in B, and Core C. The installed state is P1, A1, B1, C2. The following table is the complete compatibility information; no external package registry is involved.

Available versions: P1,P2,P3; A1,A2; B1,B2; C2,C3,C4.
A1 requires C2.
A2 requires C3 or C4.
B1 requires C2 or C3 and allows P1 or P2.
B2 requires C4 and allows P2 or P3.
There are no other platform or component constraints.

A security rule now forbids C2. A required feature requires A2. Choose a valid installation minimising the number of components whose version differs from the installed state. If plans tie on that count, choose the lexicographically smallest numerical tuple (P version, A version, B version, C version).

Report the selected versions, changed-component count, compatibility checks, and proof of minimality. Then repeat the calculation for a second, independent scenario that adds a mandatory B2 feature to the same security and A2 requirements. The second scenario also compares changes against the original installed state, not against your first proposed installation.

# Constraints

- This is a closed-book benchmark. Use the supplied evidence and rules; do not browse, run commands, or claim external verification. Any requested code or commands are proposals, not actions to execute.
- Use only listed versions and constraints; do not assume that larger versions are automatically compatible.
- Count each changed component once regardless of version distance.
- Apply the tie-break only after minimising change count.
- Keep the two independent comparisons anchored to the original state.

# Evaluation criteria

1. Models all version and feature constraints correctly.
2. Finds a compatible installation for the first scenario.
3. Finds a compatible installation for the second scenario.
4. Computes change counts and tie-breaks against the right baseline.
5. Provides a lower-bound or complete candidate argument for minimality.
