from django.utils.translation import gettext_lazy as _
import horizon

from .policy import is_requester


class BareMetalAccess(horizon.Panel):
    name = _("Bare Metal Access")
    slug = "baremetal_access"

    def allowed(self, context):
        return is_requester(context["request"].user)
