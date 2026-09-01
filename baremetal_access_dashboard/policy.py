from django.conf import settings


REQUESTER_ROLES = frozenset({"baremetal_requester", "baremetal_operator", "baremetal_admin"})


def roles(user) -> set[str]:
    return {str(role).lower() for role in (getattr(user, "roles", None) or [])}


def is_requester(user) -> bool:
    return bool(getattr(user, "tenant_id", "") and roles(user).intersection(REQUESTER_ROLES))


def is_dcn_admin(user) -> bool:
    expected = getattr(settings, "DCN_BAREMETAL_ADMIN_PROJECT_ID", "")
    return bool(expected and getattr(user, "tenant_id", "") == expected and "baremetal_admin" in roles(user))
