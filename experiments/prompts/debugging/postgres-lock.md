---
benchmark: debugging--postgres-lock
version: 2
domain: debugging
capability: database-lock-diagnosis
jurisdiction: UK
expected_output: diagnosis-and-response-plan
scoring: qualitative
---
# Task

A fictional PostgreSQL 16 checkout system has stalled updates. An administrator captured these simultaneous observations; timestamps are UTC:

pid 410: state=idle in transaction, xact_start=09:00, last query="UPDATE stock SET available=available-1 WHERE sku='A'", client=checkout-worker-2, application owner=payments team
pid 520: state=active, query_start=09:06, query="UPDATE stock SET available=available-1 WHERE sku='A'", wait_event_type=Lock, pg_blocking_pids(520)={410}
pid 530: state=active, query_start=09:07, query="ALTER TABLE stock ADD COLUMN warehouse text", wait_event_type=Lock, pg_blocking_pids(530)={410,520}
At 09:08, CPU is 12%, storage latency is normal, and no statement timeout is configured. The worker owning 410 stopped responding to its queue heartbeat at 09:01. A stock reservation can have a corresponding external payment authorization; that external side effect is not rolled back by PostgreSQL.

Explain the blocking chain and a safe immediate response, including who or what must establish transaction ownership and side effects. Compare cancelling a query with terminating a session in this specific snapshot. Propose application and database measures to prevent recurrence, plus a verification plan after intervention.

# Constraints

- This is a closed-book benchmark. Use the supplied evidence and rules; do not browse, run commands, or claim external verification. Any requested code or commands are proposals, not actions to execute.
- Do not propose killing every session, restarting PostgreSQL, or assuming a database rollback reverses external payments.
- Distinguish read-only inspection from disruptive proposed actions and state decision conditions.
- Use the supplied blocking relationships rather than inventing an exact lock-mode history.
- Do not claim CPU or query indexes explain this demonstrated lock wait.

# Evaluation criteria

1. Identifies the blocking transaction and secondary blocked work.
2. Explains cancellation versus session termination for an idle transaction.
3. Accounts for payment side effects and operational ownership.
4. Proposes proportionate recovery and recurrence prevention.
5. Checks recovery with transaction, queue, and business-state evidence.
