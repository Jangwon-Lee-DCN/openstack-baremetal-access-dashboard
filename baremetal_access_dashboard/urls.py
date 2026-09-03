from django.urls import path

from . import views

app_name = "baremetal_access"
urlpatterns = [
    path("", views.RequestListView.as_view(), name="index"),
    path("submit/", views.SubmitRequestView.as_view(), name="submit"),
    path("<uuid:request_id>/", views.RequestDetailView.as_view(), name="detail"),
    path("<uuid:request_id>/<str:action>/", views.RequestActionView.as_view(), name="action"),
]
