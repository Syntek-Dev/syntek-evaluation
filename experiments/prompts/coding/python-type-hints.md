---
benchmark: coding--python-type-hints
version: 2
domain: coding
capability: type-modelling
jurisdiction: UK
expected_output: analysis-and-code
scoring: qualitative
---
# Task

A fictional CPython 3.12 application has a cache whose values may legitimately be None. A cache hit containing None must avoid a database call. Keys are either CustomerId or OrderId; callers must not mix the two. Customer objects have name: str, while Order objects have total_pence: int. The following sketch loses these guarantees:

    cache = {}
    def get_or_load(key, loader):
        value = cache.get(key)
        if value is None:
            value = loader(key)
            cache[key] = value
        return value

Design reusable type annotations and implement get_or_load. Each entity gets its own cache instance. A loader for a CustomerId returns Customer | None, and a loader for an OrderId returns Order | None. Include minimal entity and identifier definitions, examples accepted by a strict type checker, and two examples that it should reject. Explain where static typing ends and runtime validation would be needed. Cache misses may be loaded synchronously; concurrent access and expiration are outside this fixture.

# Constraints

- This is a closed-book benchmark. Use the supplied evidence and rules; do not browse, run commands, or claim external verification. Any requested code or commands are proposals, not actions to execute.
- Use Python 3.12 standard-library typing and dataclasses; do not run or claim to run a type checker.
- Avoid Any, blanket type ignores, or casts that conceal an identifier/value mismatch.
- A loader exception must leave the cache entry absent; distinguish absence from a stored None.

# Evaluation criteria

1. Models the relationship between a cache key, its loader, and its result.
2. Distinguishes domain identifiers statically without claiming runtime enforcement.
3. Preserves cached None values and propagates loader failures correctly.
4. Shows useful positive and negative typing examples.
5. Explains relevant runtime limitations without expanding the scope.
