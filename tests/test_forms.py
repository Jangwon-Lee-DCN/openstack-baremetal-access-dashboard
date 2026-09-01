from baremetal_access_dashboard.forms import RequestForm


def test_request_form_accepts_bounded_values():
    form = RequestForm({
        "profile": "general-1u", "quantity": 2, "lease_days": 7,
        "rack": "Rack 1", "purpose": "Research workload",
    })
    assert form.is_valid(), form.errors


def test_request_form_rejects_unbounded_or_invalid_values():
    form = RequestForm({
        "profile": "../secret", "quantity": 17, "lease_days": 366,
        "rack": "Rack/1", "purpose": "x",
    })
    assert not form.is_valid()
    assert set(form.errors) == {"profile", "quantity", "lease_days", "rack", "purpose"}
