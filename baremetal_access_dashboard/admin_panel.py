from django.utils.translation import gettext_lazy as _
import horizon

from .policy import is_dcn_admin


class BareMetalApprovals(horizon.Panel):
    name = _("Bare Metal Approvals")
    slug = "baremetal_approvals"

    def allowed(self, context):
        return is_dcn_admin(context["request"].user)
