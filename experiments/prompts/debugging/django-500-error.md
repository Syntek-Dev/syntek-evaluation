---
benchmark: debugging--django-500-error
version: 2
domain: debugging
capability: serialization-boundary-debugging
jurisdiction: UK
expected_output: diagnosis-and-code
scoring: qualitative
---
# Task

A fictional Django 5.0 checkout view on Python 3.12 returns a JSON response. Order.total is a DecimalField(max_digits=12, decimal_places=2), and the application uses the default Decimal context with precision 28. The public API contract requires total_pence to be a JSON integer and currency to be "GBP". Values in this fixture are finite, nonnegative, and exactly representable in pennies; order 71 has total Decimal('12.34').

    import json
    from django.http import HttpResponse

    def detail(request, order_id):
        order = Order.objects.get(pk=order_id)
        payload = {'id': order.pk, 'total_pence': order.total, 'currency': 'GBP'}
        return HttpResponse(json.dumps(payload), content_type='application/json')

Traceback ends at json.encoder.default:
    TypeError: Object of type Decimal is not JSON serializable

Explain the immediate cause and provide a minimal corrected view. Missing orders should produce 404. Assume request authentication and object-level authorization already ran in middleware for this exercise. Include the exact JSON field values expected for order 71 and propose tests for a zero-value order and a missing order. Explain why a general-purpose encoder or converting the amount to float might suppress the exception without satisfying the API contract.

# Constraints

- This is a closed-book benchmark. Use the supplied evidence and rules; do not browse, run commands, or claim external verification. Any requested code or commands are proposals, not actions to execute.
- Use Django helpers and Decimal/integer arithmetic; no network or database execution is available.
- Do not catch every exception and return HTTP 200 or a fabricated zero total.
- Preserve integer pence in the wire format, including zero.
- State the supplied amount-validity assumption instead of adding an unrelated pricing policy.

# Evaluation criteria

1. Maps the stacktrace to the actual serialization boundary.
2. Fixes currency representation as well as exception handling.
3. Uses a clear JSON response and missing-object response.
4. Derives exact expected payload and appropriate edge-case tests.
5. Avoids masking unrelated failures or conflating serialization with authorization.
