from baremetal_access_dashboard.forms import RequestForm


def test_request_form_accepts_bounded_values():
    form = RequestForm({
        "profile": "general-1u", "quantity": 2, "lease_days": 7,
        "rack": "Rack 1", "purpose": "Research workload", "idempotency_key": "request-key-123",
    }, offers=[{"profile": "general-1u", "rack": "Rack 1"}])
    assert form.is_valid(), form.errors


def test_request_form_rejects_unbounded_or_invalid_values():
    form = RequestForm({
        "profile": "../secret", "quantity": 17, "lease_days": 366,
        "rack": "Rack/1", "purpose": "x", "idempotency_key": "short",
    }, offers=[{"profile": "general-1u", "rack": "Rack 1"}])
    assert not form.is_valid()
    assert set(form.errors) == {"idempotency_key", "profile", "quantity", "lease_days", "rack", "purpose"}
