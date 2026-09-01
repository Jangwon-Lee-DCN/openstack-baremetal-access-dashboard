from django.utils.translation import gettext_lazy as _
import horizon
import logging

from .policy import is_dcn_admin, roles


LOG = logging.getLogger(__name__)


class BareMetalApprovals(horizon.Panel):
    name = _("Bare Metal Approvals")
    slug = "baremetal_approvals"

    def allowed(self, context):
        user = context["request"].user
        allowed = is_dcn_admin(user)
        if not allowed:
            LOG.warning(
                "baremetal administrator panel denied user_id=%s project_id=%s roles=%s",
                getattr(user, "id", ""), getattr(user, "tenant_id", ""), sorted(roles(user)),
            )
        return allowed
