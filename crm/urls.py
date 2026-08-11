from django.urls import path

from . import views

app_name = "crm"

urlpatterns = [

    path(
        "",
        views.SalesDashboardView.as_view(),
        name="dashboard",
    ),

    path(
        "leads/",
        views.MyLeadsView.as_view(),
        name="my-leads",
    ),

    path(
        "leads/<int:pk>/",
        views.LeadDetailView.as_view(),
        name="lead-detail",
    ),

]