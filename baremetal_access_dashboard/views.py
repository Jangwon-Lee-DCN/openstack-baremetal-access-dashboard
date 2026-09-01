from django.contrib import messages
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import redirect
from django.views import generic

from . import client
from .forms import RequestForm
from .policy import is_dcn_admin, is_requester


class RequesterRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not is_requester(request.user):
            return HttpResponseForbidden("baremetal requester role is required")
        return super().dispatch(request, *args, **kwargs)


class AdminRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not is_dcn_admin(request.user):
            return HttpResponseForbidden("DCN baremetal administrator role is required")
        return super().dispatch(request, *args, **kwargs)


class RequestListView(RequesterRequiredMixin, generic.TemplateView):
    template_name = "baremetal_access/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["requests"] = client.request(self.request.user, "GET", "/v1/requests")
        context["offers"] = client.request(self.request.user, "GET", "/v1/offers")
        context["form"] = RequestForm(offers=context["offers"])
        return context


class SubmitRequestView(RequesterRequiredMixin, generic.View):
    def post(self, request):
        offers = client.request(request.user, "GET", "/v1/offers")
        form = RequestForm(request.POST, offers=offers)
        if not form.is_valid():
            messages.error(request, "신청 입력값을 확인하십시오.")
            return redirect("horizon:project:baremetal_access:index")
        client.request(request.user, "POST", "/v1/requests", json=form.cleaned_data)
        messages.success(request, "베어메탈 사용 신청이 등록되었습니다.")
        return redirect("horizon:project:baremetal_access:index")


class RequestActionView(RequesterRequiredMixin, generic.View):
    actions = {"cancel", "return"}

    def post(self, request, request_id, action):
        if action not in self.actions:
            raise Http404
        client.request(
            request.user, "POST", f"/v1/requests/{request_id}/{action}",
            json={"version": int(request.POST["version"])},
        )
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
