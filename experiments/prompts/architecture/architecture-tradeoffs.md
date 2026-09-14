---
benchmark: architecture--architecture-tradeoffs
version: 2
domain: architecture
capability: architecture-decision-analysis
jurisdiction: UK
expected_output: decision-record
scoring: qualitative
---
# Task

Write a short architecture decision record for a fictional UK software team. Four engineers maintain an order-management application used by 120 internal staff. It processes 8 requests/second on average and peaks at 40; current p95 latency is 180 ms against a 500 ms objective. Deployments occur twice weekly. The most frequent incident is an external tax-calculation service timing out and exhausting the application worker pool. Reporting jobs also consume the primary database connection pool for roughly ten minutes each morning. A proposed rewrite splits the application into 12 microservices and introduces a message broker, service mesh and separate database per service. The team has no dedicated platform engineer, and next quarter must ship a new warehouse workflow.

Compare retaining a modular application with targeted isolation, splitting a small number of components, and the full proposal. Recommend a decision tied to the supplied evidence; include boundaries, timeout/resource controls, transaction implications, rollout/reversal and measurable triggers for reconsideration. The head of engineering prefers microservices, while operations wants no architectural changes. Explain how you would resolve that disagreement with experiments. Do not assume either preference is a technical requirement or that the current latency figure explains the incident mechanism.

# Constraints

- This is a closed-book benchmark. Use the supplied evidence and rules; do not browse, run commands, or claim external verification. Any requested code or commands are proposals, not actions to execute.
- State unknowns and identify the smallest measurements needed to resolve them.
- Do not claim a service mesh fixes unbounded application concurrency or poor database query scheduling by itself.
- Account for team capacity and the warehouse delivery commitment.
- Give at least one credible benefit and cost for each option; avoid a generic microservices slogan.

# Evaluation criteria

1. Connects recommendations to incident mechanisms, workload and staffing.
2. Compares alternatives fairly with explicit tradeoffs.
3. Defines focused resilience and resource-isolation changes.
4. Provides measurable experiments, rollout and reversal.
5. Sets evidence-based reconsideration triggers and handles stakeholder disagreement.
