from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path


urlpatterns = [

    # -------------------------
    # Django Administration
    # -------------------------
    path(
        "admin/",
        admin.site.urls,
    ),

    # -------------------------
    # Public Website
    # -------------------------
    path(
        "",
        include("website.urls"),
    ),

    # -------------------------
    # Customer Portal
    # -------------------------
    path(
        "portal/",
        include("customer_portal.urls"),
    ),

    # -------------------------
    # Authentication
    # -------------------------
    path(
        "accounts/",
        include("accounts.urls"),
    ),

    # -------------------------
    # Staff Portal
    # -------------------------
    path(
        "staff/",
        include("dashboard.urls"),
    ),

    path(
        "staff/customers/",
        include("customers.urls"),
    ),

    path(
        "staff/assessments/",
        include("audits.urls"),
    ),

    path(
        "staff/equipment/",
        include("equipment.urls"),
    ),

    path(
        "staff/reports/",
        include("reports.urls"),
    ),

    path(
        "staff/quotations/",
        include(("quotations.urls", "quotations"), namespace="quotations"),
    ),

    # -------------------------
    # CRM
    # -------------------------

    path(
        "staff/crm/",
        include("crm.urls"),
    ),

    path(
        "staff/administration/",
        include("administration.urls"),
    ),

]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )