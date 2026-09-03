from django.conf import settings


REQUESTER_ROLES = frozenset({"baremetal_requester", "baremetal_operator", "baremetal_admin"})
PROJECT_MEMBER_ROLES = frozenset({"member", "admin"})
OPERATOR_ROLES = frozenset({"baremetal_operator", "baremetal_admin", "admin"})


def roles(user) -> set[str]:
    names = set()
    for role in getattr(user, "roles", None) or []:
        name = role.get("name") if isinstance(role, dict) else role
        if name:
            names.add(str(name).lower())
    return names


def is_requester(user) -> bool:
    if not getattr(user, "tenant_id", ""):
        return False
    assigned = roles(user)
    expected_domain = getattr(settings, "DCN_BAREMETAL_DOMAIN_ID", "")
    user_domain = getattr(user, "user_domain_id", "") or getattr(user, "domain_id", "")
    return bool(
        expected_domain and user_domain == expected_domain
        and assigned.intersection(REQUESTER_ROLES | PROJECT_MEMBER_ROLES)
    )


def is_operator(user) -> bool:
    if not is_requester(user):
        return False
    return bool(roles(user).intersection(OPERATOR_ROLES))


def is_dcn_admin(user) -> bool:
    expected = getattr(settings, "DCN_BAREMETAL_ADMIN_PROJECT_ID", "")
    return bool(expected and getattr(user, "tenant_id", "") == expected and "baremetal_admin" in roles(user))
