from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_request_table_carries_deterministic_purpose_and_node_state():
    template = (ROOT / "baremetal_access_dashboard/templates/baremetal_access/index.html").read_text()
    assert "{{ item.purpose }}" in template
    assert 'data-request-id="{{ item.id }}"' in template
    assert 'data-request-state="{{ item.state }}"' in template
    assert 'id="baremetal-resource-table"' in template
    assert "Request Bare Metal" in template
    assert 'id="request-baremetal-modal"' in template
    assert "Launch Bare Metal" in template
    assert "baremetal-deploy" in template
    assert "baremetal-operations" in template
    assert 'name="idempotency_key"' in template
    assert "and can_operate" in template


def test_detail_page_shows_sanitized_lease_and_operation_history():
    template = (ROOT / "baremetal_access_dashboard/templates/baremetal_access/detail.html").read_text()
    assert "Request and lease" in template
    assert "Assigned hardware" in template
    assert "Operation history" in template
    assert 'data-operation-state="{{ operation.state }}"' in template
    for forbidden in ("bmc_address", "driver_info", "password", "serial_number"):
        assert forbidden not in template


def test_request_modal_uses_horizon_form_structure_and_guidance():
    template = (ROOT / "baremetal_access_dashboard/templates/baremetal_access/index.html").read_text()
    assert "{{ form.as_p }}" not in template
    assert "form.visible_fields" in template
    assert "form-group" in template
    assert "control-label" in template
    assert "help-block" in template
    assert "hz-icon-required" in template
    assert "baremetal-request-help" in template
    assert "No bare metal capacity is currently available." in template
    assert 'type="submit"{% if not offers %} disabled{% endif %}' in template


def test_request_modal_styles_are_responsive():
    stylesheet = (ROOT / "baremetal_access_dashboard/static/baremetal_access/css/baremetal_access.css").read_text()
    assert ".baremetal-request-dialog" in stylesheet
    assert "min(760px, calc(100% - 30px))" in stylesheet
    assert "@media (max-width: 767px)" in stylesheet
