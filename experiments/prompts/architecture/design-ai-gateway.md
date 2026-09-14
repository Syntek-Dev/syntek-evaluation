---
benchmark: architecture--design-ai-gateway
version: 2
domain: architecture
capability: ai-gateway-design
jurisdiction: UK
expected_output: architecture-and-capacity-analysis
scoring: qualitative
---
# Task

Design an internal AI gateway for a fictional UK engineering company. Applications send authenticated requests containing tenant_id, task_class, sensitivity, a prompt, and a client deadline. The gateway serves two local inference backends with 12 and 8 concurrent-request slots respectively. For this capacity exercise every successful inference occupies one slot for exactly two seconds; networking and routing overhead are negligible. Expected sustained arrival rate is 15 requests/second, with short bursts of 30. No new hardware is available this quarter. External providers are forbidden for confidential data and permitted for public data, which accounts for 40% of sustained requests. Public requests may also use local backends.

Specify the request path, authentication/tenant enforcement, queue and admission rules, cancellation, backend health handling, and redacted observability. Calculate sustainable local throughput and assess whether routing all permitted public traffic externally resolves steady-state capacity. Explain why deadlines and overload responses still matter after routing. Include a short failure walkthrough in which a local backend fails after accepting a confidential request, and state when retrying could violate the deadline or repeat side effects. Output a compact architecture description, capacity calculation, and five rollout acceptance checks.

# Constraints

- This is a closed-book benchmark. Use the supplied evidence and rules; do not browse, run commands, or claim external verification. Any requested code or commands are proposals, not actions to execute.
- Treat all workloads and timings as fixed synthetic inputs; do not invent provider capacities or measured latencies.
- Sensitivity and tenant identity must be enforced from trusted policy/identity, not accepted solely from client fields.
- Use bounded queues and a stated overload policy; do not assume buffering creates throughput.
- Do not persist raw confidential prompts in ordinary logs.

# Evaluation criteria

1. Calculates capacity and remaining load with the stated units.
2. Separates identity, policy, routing, admission, and inference responsibilities.
3. Handles overload, deadlines, cancellation, and backend failures coherently.
4. Protects tenant data and constrains external fallback.
5. Provides measurable checks and acknowledges unproven external capacity.
