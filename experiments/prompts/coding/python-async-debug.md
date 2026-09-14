---
benchmark: coding--python-async-debug
version: 2
domain: coding
capability: async-concurrency
jurisdiction: UK
expected_output: analysis-and-code
scoring: qualitative
---
# Task

A fictional Python 3.12 service calls an injected async function fetch_one(url), which either returns bytes or raises. This batch wrapper is used inside an already-running asyncio event loop:

    async def fetch_all(urls, fetch_one):
        tasks = []
        for url in urls:
            tasks.append(asyncio.create_task(fetch_one(url)))
            time.sleep(0.05)
        return [task.result() for task in tasks]

Replace it under this contract: return results in input order; allow at most four fetch_one calls in progress at once; a two-second batch deadline initiates cancellation of outstanding work; a child failure or caller cancellation also cancels and awaits outstanding work. Cancellation cleanup may finish after the two-second deadline, and the wrapper must await it before returning or raising. The two seconds is a cancellation-initiation target on a responsive event loop, not a hard upper bound on complete cleanup. Empty input returns []. The input contains at most 100 URLs. A fetch operation is cancellation-cooperative; you do not need to handle a coroutine that deliberately suppresses cancellation. Describe what callers observe for timeout, cancellation, and a child exception. Include a deterministic test strategy using events or counters rather than depending on wall-clock races. An ExceptionGroup for child failures is acceptable if you explain it.

# Constraints

- This is a closed-book benchmark. Use the supplied evidence and rules; do not browse, run commands, or claim external verification. Any requested code or commands are proposals, not actions to execute.
- Use asyncio from Python 3.12 only; do not introduce asyncio.run inside the wrapper.
- Do not block the event-loop thread or swallow CancelledError.
- Start the batch deadline when the wrapper begins scheduling work. Initiate timeout cancellation at two seconds, then await cleanup before returning or raising; cleanup may extend total elapsed time.

# Evaluation criteria

1. Explains scheduling and result-access errors in the supplied code.
2. Bounds active I/O while retaining input order.
3. Applies the batch cancellation deadline and reliably awaits child cleanup, without claiming a hard two-second completion bound.
4. Accurately describes exception and cancellation behaviour.
5. Offers tests capable of detecting concurrency and cleanup regressions.
