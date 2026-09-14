---
benchmark: architecture--design-multi-tenant-saas
version: 2
domain: architecture
capability: tenant-isolation-design
jurisdiction: UK
expected_output: architecture-and-migration-plan
scoring: qualitative
---
# Task

A fictional B2B SaaS product serves 80 tenants through a Django 5.0 API and PostgreSQL 16 database. Most tenants have fewer than 20 users; one tenant produces 55% of background export work. The current shared schema stores tenant_id on invoices and customers. A proposal relies on every developer remembering to add filter(tenant_id=request.headers['X-Tenant']) to each query. Background jobs carry tenant_id in their message body. Redis caches use keys like invoice:123, and exports are placed in object storage under invoices/{invoice_id}. There are no contractual requirements for a database per tenant. A three-person team maintains the system.

Recommend a proportionate isolation design and migration plan. Cover the source of trusted tenant identity, relational constraints, queries and database defence in depth, background jobs, caches, object access, administrative support access and resource fairness. Compare shared-schema and per-tenant-database approaches using these workload facts. Include a concrete negative test that attempts to relate an invoice in one tenant to a customer in another, and explain how migration can discover and remediate existing cross-tenant inconsistencies without automatically deleting financial records.

# Constraints

- This is a closed-book benchmark. Use the supplied evidence and rules; do not browse, run commands, or claim external verification. Any requested code or commands are proposals, not actions to execute.
- Do not trust a tenant header or queue field without binding it to an authenticated/authorized context.
- Do not assume row-level security alone protects caches, objects, logs or privileged support tools.
- Preserve existing data during migration and make anomalies reviewable.
- Do not make unsupported legal/compliance claims about the required isolation level.

# Evaluation criteria

1. Identifies concrete tenant-boundary failures across the supplied system.
2. Proposes enforceable relational and request-level isolation.
3. Accounts for jobs, caches, objects and support access.
4. Addresses the dominant tenant workload and operational tradeoffs.
5. Plans staged validation/migration with meaningful cross-tenant tests.
