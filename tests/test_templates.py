from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_request_table_carries_deterministic_purpose_and_node_state():
    template = (ROOT / "baremetal_access_dashboard/templates/baremetal_access/index.html").read_text()
    assert "{{ item.purpose }}" in template
    assert 'data-request-id="{{ item.id }}"' in template
    assert "{{ item.state }}" in template
    assert "{{ node }}" in template
