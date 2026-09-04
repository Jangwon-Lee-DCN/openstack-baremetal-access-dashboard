from baremetal_access_dashboard.forms import DeployForm, PowerForm, RequestForm


def test_request_form_accepts_bounded_values():
    form = RequestForm({
        "profile": "general-1u", "quantity": 2, "lease_days": 7,
        "rack": "Rack 1", "purpose": "Research workload", "idempotency_key": "request-key-123",
    }, offers=[{"profile": "general-1u", "rack": "Rack 1"}])
    assert form.is_valid(), form.errors


def test_request_form_uses_horizon_sized_controls_and_defaults():
    form = RequestForm(offers=[{"profile": "general-1u", "rack": "Rack 1"}])
    assert form.fields["quantity"].initial == 1
    assert form.fields["lease_days"].initial == 1
    assert form.fields["purpose"].widget.attrs["rows"] == 5
    assert all(
        field.widget.attrs.get("class") == "form-control"
        for name, field in form.fields.items() if name != "idempotency_key"
    )
    assert form.fields["rack"].choices[0] == ("", "No preference (any eligible rack)")


def test_request_form_rejects_unbounded_or_invalid_values():
    form = RequestForm({
        "profile": "../secret", "quantity": 17, "lease_days": 366,
        "rack": "Rack/1", "purpose": "x", "idempotency_key": "short",
    }, offers=[{"profile": "general-1u", "rack": "Rack 1"}])
    assert not form.is_valid()
    assert set(form.errors) == {"idempotency_key", "profile", "quantity", "lease_days", "rack", "purpose"}


def test_deploy_and_power_forms_are_allowlisted():
    node = "11111111-1111-1111-1111-111111111111"
    image = "22222222-2222-2222-2222-222222222222"
    deploy = DeployForm(
        {"idempotency_key": "deploy-key-123", "version": 3, "node_uuid": node,
         "image_id": image, "hostname": "research-01"},
        images=[{"id": image, "name": "Ubuntu"}],
    )
    assert deploy.is_valid(), deploy.errors
    assert not PowerForm({"idempotency_key": "power-key-123", "version": 3,
                          "node_uuid": node, "action": "maintenance"}).is_valid()
