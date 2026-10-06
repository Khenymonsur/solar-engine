from django.urls import path

from . import views

app_name = "administration"

urlpatterns = [

    path(
        "",
        views.AdministrationDashboardView.as_view(),
        name="dashboard",
    ),

    path(
        "users/",
        views.UserListView.as_view(),
        name="user-list",
    ),

    path(
        "users/<int:pk>/edit/",
        views.StaffUserUpdateView.as_view(),
        name="user-edit",
    ),

    path(
        "users/create/",
        views.StaffUserCreateView.as_view(),
        name="user-create",
    ),

    path(
            "users/<int:pk>/",
            views.StaffProfileView.as_view(),
            name="user-detail",
        ),

    path(
        "roles/",
        views.RoleListView.as_view(),
        name="role-list",
    ),

    path(
        "roles/create/",
        views.RoleCreateView.as_view(),
        name="role-create",
    ),

    path(
        "roles/<int:pk>/",
        views.RoleDetailView.as_view(),
        name="role-detail",
    ),

    path(
        "roles/<int:pk>/edit/",
        views.RoleUpdateView.as_view(),
        name="role-edit",
    ),

    path(
        "users/<int:pk>/roles/",
        views.StaffRoleUpdateView.as_view(),
        name="user-roles",
    ),

    path(
        "users/<int:pk>/toggle-status/",
        views.StaffAccountStatusView.as_view(),
        name="user-toggle-status",
    ),




]