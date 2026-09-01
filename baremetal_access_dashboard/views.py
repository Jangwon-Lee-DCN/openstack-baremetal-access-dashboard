from django.contrib import messages
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import redirect
from django.views import generic
import logging
from uuid import uuid4

from . import client
from .forms import DeployForm, PowerForm, RequestForm
from .policy import is_dcn_admin, is_requester, roles


LOG = logging.getLogger(__name__)


class RequesterRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not is_requester(request.user):
            LOG.warning(
                "baremetal requester denied user_id=%s project_id=%s roles=%s",
                getattr(request.user, "id", ""),
                getattr(request.user, "tenant_id", ""),
                sorted(roles(request.user)),
            )
            return HttpResponseForbidden("baremetal requester role is required")
        return super().dispatch(request, *args, **kwargs)


class AdminRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not is_dcn_admin(request.user):
            LOG.warning(
                "baremetal administrator denied user_id=%s project_id=%s roles=%s",
                getattr(request.user, "id", ""),
                getattr(request.user, "tenant_id", ""),
                sorted(roles(request.user)),
            )
            return HttpResponseForbidden("DCN baremetal administrator role is required")
        return super().dispatch(request, *args, **kwargs)


class RequestListView(RequesterRequiredMixin, generic.TemplateView):
    template_name = "baremetal_access/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["requests"] = client.request(self.request.user, "GET", "/v1/requests")
        for item in context["requests"]:
            item["operations"] = client.request(
                self.request.user, "GET", f"/v1/requests/{item['id']}/operations",
            )
            item["node_controls"] = [
                {"uuid": node, "deploy_key": str(uuid4()), "power_key": str(uuid4())}
                for node in item.get("nodes", [])
            ]
        context["offers"] = client.request(self.request.user, "GET", "/v1/offers")
        context["deploy_images"] = client.request(self.request.user, "GET", "/v1/deploy-images")
        context["can_operate"] = bool(roles(self.request.user).intersection({"baremetal_operator", "baremetal_admin"}))
        context["form"] = RequestForm(offers=context["offers"])
        return context


class SubmitRequestView(RequesterRequiredMixin, generic.View):
    def post(self, request):
        offers = client.request(request.user, "GET", "/v1/offers")
        form = RequestForm(request.POST, offers=offers)
        if not form.is_valid():
            messages.error(request, "신청 입력값을 확인하십시오.")
            return redirect("horizon:project:baremetal_access:index")
        payload = dict(form.cleaned_data)
        idempotency_key = payload.pop("idempotency_key")
        client.request(
            request.user, "POST", "/v1/requests", json=payload,
            idempotency_key=idempotency_key,
        )
        messages.success(request, "베어메탈 사용 신청이 등록되었습니다.")
        return redirect("horizon:project:baremetal_access:index")


class RequestActionView(RequesterRequiredMixin, generic.View):
    actions = {"cancel", "return", "deploy", "power"}

    def post(self, request, request_id, action):
        if action not in self.actions:
            raise Http404
        if action == "deploy":
            images = client.request(request.user, "GET", "/v1/deploy-images")
            form = DeployForm(request.POST, images=images)
        elif action == "power":
            form = PowerForm(request.POST)
        else:
            form = None
        if form is not None:
            if not form.is_valid():
                messages.error(request, "노드 작업 입력값을 확인하십시오.")
                return redirect("horizon:project:baremetal_access:index")
            payload = form.cleaned_data
            idempotency_key = payload.pop("idempotency_key")
            payload["node_uuid"] = str(payload["node_uuid"])
        else:
            payload = {"version": int(request.POST["version"])}
            idempotency_key = None
        client.request(
            request.user, "POST", f"/v1/requests/{request_id}/{action}", json=payload,
            idempotency_key=idempotency_key,
        )
        if action in {"deploy", "power"}:
            messages.success(request, "노드 작업이 큐에 등록되었습니다.")
        else:
            messages.success(request, "요청 상태가 변경되었습니다.")
        return redirect("horizon:project:baremetal_access:index")


class ApprovalListView(AdminRequiredMixin, generic.TemplateView):
    template_name = "baremetal_access/admin.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["requests"] = client.request(self.request.user, "GET", "/v1/admin/requests")
        return context


class AdminActionView(AdminRequiredMixin, generic.View):
    actions = {"approve", "reject"}

    def post(self, request, request_id, action):
        if action not in self.actions:
            raise Http404
        payload = {"version": int(request.POST["version"])}
        if action == "reject":
            payload["reason"] = request.POST.get("reason", "").strip()
        client.request(
            request.user, "POST", f"/v1/admin/requests/{request_id}/{action}", json=payload,
        )
        messages.success(request, "관리자 결정이 반영되었습니다.")
        return redirect("horizon:admin:baremetal_approvals:index")
