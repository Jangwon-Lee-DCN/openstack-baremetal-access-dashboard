from django.urls import path

from . import views

app_name = "baremetal_approvals"
urlpatterns = [
    path("", views.ApprovalListView.as_view(), name="index"),
    path("<uuid:request_id>/<str:action>/", views.AdminActionView.as_view(), name="action"),
]
