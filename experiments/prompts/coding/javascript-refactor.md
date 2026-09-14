---
benchmark: coding--javascript-refactor
version: 2
domain: coding
capability: async-javascript-refactor
jurisdiction: UK
expected_output: analysis-and-code
scoring: qualitative
---
# Task

A fictional service runs Node.js 20. Each input row is {id: string, enabled: boolean}. load(id) returns a Promise for an object, or rejects. Refactor the following function so it returns a Promise of the loaded objects for enabled rows in original order. Duplicate enabled IDs should trigger one load call per distinct ID, but their results must appear at each original position. Disabled rows must not trigger loads. On any load failure reject the whole operation; handling cancellation of already-started I/O is outside scope. The input has at most 100 rows, and concurrent loads are allowed.

    function hydrate(rows, load) {
      const result = [];
      rows.forEach(async row => {
        if (row.enabled) {
          row.item = await load(row.id);
          result.push(row.item);
        }
      });
      return result;
    }

Show the replacement and explain timing, error propagation, and mutation problems in the original. Demonstrate behaviour with enabled IDs ['b', 'a', 'b'] when a resolves first. State whether duplicate positions intentionally share the same returned object and why that is acceptable under this contract.

# Constraints

- This is a closed-book benchmark. Use the supplied evidence and rules; do not browse, run commands, or claim external verification. Any requested code or commands are proposals, not actions to execute.
- Use standard JavaScript with native promises; do not mutate rows or loaded objects.
- Assume rows are already validated; do not add truthy coercion rules.
- Handle both a synchronous throw from load and a rejected promise.
- Do not claim Promise.all cancels the underlying operations.

# Evaluation criteria

1. Explains why async forEach does not provide awaited completion.
2. Returns an awaited result in input order and propagates failures.
3. Deduplicates work without deduplicating output positions.
4. Avoids input mutation and documents result object identity.
5. Demonstrates observable behaviour under out-of-order completion.
