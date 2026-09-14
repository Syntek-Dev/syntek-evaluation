---
benchmark: architecture--design-local-ai-cluster
version: 2
domain: architecture
capability: local-inference-capacity-design
jurisdiction: UK
expected_output: deployment-design-and-calculations
scoring: qualitative
---
# Task

Plan a fictional local inference cluster using only the hardware and fixed model measurements below. Host A has two 24 GiB GPUs; Host B has one 24 GiB GPU. Each GPU must retain 2 GiB unallocated operating headroom. Model Small uses 12 GiB of weights plus 4 GiB of KV cache per serving replica and sustains 6 requests/second at the target context length. It runs on one GPU. Model Large uses 26 GiB of weights plus 6 GiB KV cache per replica; the runtime supports even tensor parallel splitting across the two GPUs within Host A, with the quoted memory divided equally. Large sustains 4 requests/second per two-GPU replica. Cross-host tensor parallelism and CPU offload are unsupported. Memory and throughput figures already include all other runtime overhead.

Required sustained traffic is 7 requests/second for tasks approved only on Small and 2 requests/second for tasks approved only on Large. Each traffic class must use its respective validated model; cross-model substitution is not approved, even when another model has spare throughput. Design a placement or demonstrate why these requirements cannot all be met. Explain the effect of losing either host. Propose the smallest product-level concession or hardware change needed, without inventing new benchmark rates. Include admission control, monitoring and a validation plan for longer contexts, which were not measured.

# Constraints

- This is a closed-book benchmark. Use the supplied evidence and rules; do not browse, run commands, or claim external verification. Any requested code or commands are proposals, not actions to execute.
- Use GiB consistently and account for headroom on each GPU.
- Do not silently run Large on a single GPU or combine memory across hosts.
- Do not substitute either model for the other traffic class; approval is specific to the model and task class.
- Distinguish nominal placement capacity from resilience and unmeasured longer-context capacity.

# Evaluation criteria

1. Derives valid placements from per-GPU memory constraints.
2. Calculates throughput against both task classes.
3. Identifies infeasibility or bottlenecks explicitly.
4. Analyses host failure and practical tradeoffs.
5. Includes controls and measurements needed before deployment.
