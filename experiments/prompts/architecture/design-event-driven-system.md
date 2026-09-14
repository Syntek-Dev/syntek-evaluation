---
benchmark: architecture--design-event-driven-system
version: 2
domain: architecture
capability: event-consistency-design
jurisdiction: UK
expected_output: architecture-and-failure-walkthrough
scoring: qualitative
---
# Task

A fictional order service on PostgreSQL 16 publishes OrderPlaced events to a message broker. Delivery is at least once and events for different orders can arrive in any order. The service currently commits the order row, then publishes an event. Occasionally a process crash between those operations leaves an order that inventory never sees. Publishing before the database commit was suggested as a fix. Inventory and billing use separate databases. An external payment API supports a caller-supplied idempotency key retained for seven days. An order may be cancelled while inventory reservation is still being retried.

Propose a design that closes the database/publish gap and gives inventory and billing repeatable processing. Walk through a crash after publication but before acknowledgment, duplicate delivery, a payment success followed by a consumer crash, and cancellation racing with reservation. Define event identifiers, order/version handling, consumer state, retry/dead-letter rules and an operational reconciliation process. Distinguish exactly-once business effects from transport claims. The system processes 20 orders/second, so prefer a design a small team can operate without adding a new consensus system.

# Constraints

- This is a closed-book benchmark. Use the supplied evidence and rules; do not browse, run commands, or claim external verification. Any requested code or commands are proposals, not actions to execute.
- Do not assume a transaction spanning PostgreSQL, the broker and the payment provider.
- Do not claim at-least-once delivery can be turned into exactly-once effects merely by choosing a broker option.
- Use explicit state transitions and idempotency; account for the seven-day payment-key horizon.
- Include observability and recovery for poison messages without silently dropping them.

# Evaluation criteria

1. Closes the dual-write gap with a durable publication mechanism.
2. Handles duplicate delivery and external side effects coherently.
3. Resolves cancellation/reservation ordering through explicit business state.
4. Defines bounded retries, reconciliation and dead-letter handling.
5. States guarantees and residual limitations precisely.
