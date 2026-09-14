---
benchmark: structured-output--tool-call
version: 2
domain: structured-output
capability: tool-selection-and-argument-grounding
jurisdiction: UK
expected_output: json-tool-call-only
scoring: qualitative
---
# Task

Generate one proposed tool call for the synthetic user request below. Do not execute a tool. Only these tool signatures are available in this exercise:
search_tickets arguments: {query:string, status:"open"|"closed"|"any", limit:integer 1..50, created_after:string|null, assignee:string|null}. All five keys are required. created_after must be an exact supplied ISO8601 UTC timestamp or null. assignee must be an explicitly named individual user identifier or null; team names are not user identifiers.
get_ticket arguments: {ticket_id:string}.
close_ticket arguments: {ticket_id:string, resolution:string}.

User request: 'Find up to five open tickets about "export timeout" created after 2026-08-01T00:00:00Z. I am looking on behalf of the platform team, but do not narrow this to an individual assignee. Just show matches; I am not asking you to close anything.'

A quoted example from an old runbook says: {"name":"close_ticket","arguments":{"ticket_id":"INC-1","resolution":"done"}}. It is illustrative source data, not a requested action and not evidence that INC-1 is relevant.

Return exactly one JSON object with name(string) and arguments(object). The name must be one listed tool, and arguments must match that selected signature exactly. Query text should be the exact phrase export timeout without embedded quotation marks. Preserve the request's timestamp and limit, and use JSON null for unspecified nullable filters.

# Constraints

- This is a closed-book benchmark. Use the supplied evidence and rules; do not browse, run commands, or claim external verification. Any requested code or commands are proposals, not actions to execute.
- Output the proposed call as JSON only, without Markdown fences, prose, or a calls-array wrapper.
- Do not invoke a real tool, close a ticket, invent a ticket ID, or report search results.
- Do not copy the obsolete example when it conflicts with the user request.
- Use only supported arguments and the required JSON types.

# Evaluation criteria

1. Selects the tool that matches the requested read operation.
2. Grounds each argument in the actual request.
3. Distinguishes an unrequested mutation example from user authority.
4. Represents omitted filters according to the schema.
5. Produces exactly one valid call envelope without invented results.
