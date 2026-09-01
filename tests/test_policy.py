from types import SimpleNamespace

from baremetal_access_dashboard.policy import is_dcn_admin, is_requester, roles


def user(project, roles):
    return SimpleNamespace(tenant_id=project, roles=roles)


def test_requester_requires_project_scope_and_explicit_role():
    assert is_requester(user("tenant-a", ["baremetal_requester"]))
    assert is_requester(user("tenant-a", [{"name": "baremetal_requester"}]))
    assert not is_requester(user("", ["baremetal_requester"]))
    assert not is_requester(user("tenant-a", ["member"]))


def test_admin_requires_exact_dcn_project_and_role():
    assert is_dcn_admin(user("dcn-project", ["baremetal_admin"]))
    assert is_dcn_admin(user("dcn-project", [{"name": "baremetal_admin"}]))
    assert not is_dcn_admin(user("other-project", ["baremetal_admin"]))
    assert not is_dcn_admin(user("dcn-project", ["admin"]))


def test_role_parser_ignores_malformed_runtime_entries():
    assert roles(user("tenant-a", [{"name": "BareMetal_Operator"}, {}, None])) == {
        "baremetal_operator",
    }
