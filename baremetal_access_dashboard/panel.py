from django.utils.translation import gettext_lazy as _
import horizon
import logging

from .policy import is_requester, roles


LOG = logging.getLogger(__name__)


class BareMetalAccess(horizon.Panel):
    name = _("Bare Metal Access")
    slug = "baremetal_access"

    def allowed(self, context):
        user = context["request"].user
        allowed = is_requester(user)
        if not allowed:
            LOG.warning(
                "baremetal requester panel denied user_id=%s project_id=%s roles=%s",
                getattr(user, "id", ""), getattr(user, "tenant_id", ""), sorted(roles(user)),
            )
        return allowed
