---
benchmark: reasoning--conflicting-requirements
version: 2
domain: reasoning
capability: requirements-feasibility
jurisdiction: UK
expected_output: feasibility-analysis-and-options
scoring: qualitative
---
# Task

A fictional key-value store receives three proposed requirements for every accepted write:
A. The client receives a successful acknowledgement within 10 ms of the request reaching region North.
B. Before that acknowledgement, the value is durably stored in both North and South and North has confirmation of South's durable completion.
C. Writes remain available during a complete North-South network partition lasting up to one hour, meaning North must continue acknowledging new writes successfully.

In the supplied model, a request arrives first in North. North-to-South propagation is at least 11 ms and South-to-North propagation is at least 11 ms. Durable storage and local computation take a non-negative amount of time. There is no alternate communication path, pre-shared copy of future write values, or external arbiter that can communicate across the partition. Rejected, queued, or timed-out requests do not count as available writes. These are hard per-write guarantees, not percentile targets.

Assess joint feasibility. Identify conflicts with an explicit timing bound and a partition argument. Propose three concrete revised requirement packages, stating which promises each preserves and relaxes, how clients would observe the behavior, and what outstanding product choice is needed before implementation.

# Constraints

- This is a closed-book benchmark. Use the supplied evidence and rules; do not browse, run commands, or claim external verification. Any requested code or commands are proposals, not actions to execute.
- Use the model exactly; do not invent faster links, hidden replicas, or probabilistic exceptions.
- Keep durable replication distinct from sending a message toward the other region.
- Do not silently reinterpret success, availability, or the 10 ms deadline.
- Make tradeoffs explicit without choosing business priorities on the stakeholder behalf.

# Evaluation criteria

1. Derives the relevant communication lower bound.
2. Analyses partition behavior using the defined success semantics.
3. Identifies incompatible guarantees without hiding them in implementation details.
4. Presents concrete revised packages with understandable client behavior.
5. States the stakeholder decision needed to resolve the conflict.
