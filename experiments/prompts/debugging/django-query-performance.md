---
benchmark: debugging--django-query-performance
version: 2
domain: debugging
capability: orm-query-diagnosis
jurisdiction: UK
expected_output: diagnosis-and-code
scoring: qualitative
---
# Task

A fictional Django 5.0 application on PostgreSQL 16 renders a paginated list of 50 projects. Project has ForeignKey owner to User and related_name tasks from Task. The template prints project.owner.username and project.tasks.filter(status='open').count(). Projects are ordered by id. No custom managers, signals, or template tags issue database queries. A debug trace shows one COUNT for pagination, one SELECT for the 50 projects, 50 User SELECTs, and 50 Task COUNTs. The endpoint is correct but slow when network latency to PostgreSQL increases.

Current view sketch:
    page = Paginator(Project.objects.order_by('id'), 50).get_page(request.GET.get('page'))

Current template fragment:
    {{ project.owner.username }} {{ project.tasks.filter(status='open').count }}

For this fixture the template fragment denotes the described Python ORM access; you may replace it with valid Django template fields. Explain the query pattern and provide a corrected queryset/template approach. A project with zero open tasks must remain in the page and display zero. Propose meaningful verification of both counts and query volume, and explain what could change the exact query count in a real deployment.

# Constraints

- This is a closed-book benchmark. Use the supplied evidence and rules; do not browse, run commands, or claim external verification. Any requested code or commands are proposals, not actions to execute.
- Do not remove pagination, drop zero-task projects, or cache stale task counts as a shortcut.
- Use supported Django 5.0 ORM concepts; no raw SQL or external tools is necessary.
- Do not claim indexes alone eliminate per-object queries.
- Distinguish the supplied idealised trace from measurements you have not made.

# Evaluation criteria

1. Derives the baseline query volume and identifies both repeated access patterns.
2. Fetches owners and open-task counts without per-project queries.
3. Preserves pagination, ordering, and zero-count semantics.
4. Updates rendering to use precomputed attributes correctly.
5. Describes tests for correctness and query volume with realistic qualifications.
