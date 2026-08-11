from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)

from django.contrib import messages
from django.urls import reverse_lazy

from django.views.generic import (
    CreateView,
    ListView,
    TemplateView,
    UpdateView,
)

from .forms import (
    StaffUserCreateForm,
    StaffUserForm,
)

from django.db.models import Q

from django.contrib.auth.models import Group, Permission
from django.views.generic import DetailView


User = get_user_model()


class AdministrationDashboardView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    TemplateView,
):
    """
    Administration Home
    """

    permission_required = "auth.view_user"

    template_name = "administration/dashboard.html"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        staff = User.objects.filter(is_staff=True)
        context["total_users"] = staff.count()
        context["active_users"] = staff.filter(
            is_active=True
        ).count()
        context["inactive_users"] = staff.filter(
            is_active=False
        ).count()
        context["recent_users"] = (
            staff
            .prefetch_related("groups")
            .order_by("-date_joined")[:5]
        )

        return context


class UserListView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    ListView,
):
    permission_required = "auth.view_user"

    model = User

    template_name = "administration/user_list.html"

    context_object_name = "users"

    paginate_by = 20

    def get_queryset(self):
        queryset = (
            User.objects
            .filter(is_staff=True)
            .prefetch_related("groups")
            .order_by("first_name", "last_name")
        )

        role = self.request.GET.get("role")

        if role:
            queryset = queryset.filter(
                groups__id=role
            )

        status = self.request.GET.get("status")

        if status == "active":
            queryset = queryset.filter(is_active=True)

        elif status == "inactive":
            queryset = queryset.filter(is_active=False)

        search = self.request.GET.get("search")

        if search:
            queryset = queryset.filter(
                Q(first_name__icontains=search)
                | Q(last_name__icontains=search)
                | Q(username__icontains=search)
                | Q(email__icontains=search)
            )

        return queryset



    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["roles"] = Group.objects.order_by("name")

        return context





class StaffUserUpdateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UpdateView,
):
    """
    Edit Staff User
    """

    permission_required = "auth.change_user"

    model = User

    form_class = StaffUserForm

    template_name = "administration/user_form.html"

    success_url = reverse_lazy(
        "administration:user-list"
    )

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["page_title"] = "Edit Staff User"

        return context




class StaffUserCreateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    CreateView,
):
    permission_required = "auth.add_user"

    model = User

    form_class = StaffUserCreateForm

    template_name = "administration/user_create.html"

    success_url = reverse_lazy(
        "administration:user-list"
    )

    def form_valid(self, form):
        response = super().form_valid(form)

        messages.success(
            self.request,
            f"Staff user '{self.object.get_full_name() or self.object.username}' "
            "was created successfully."
        )

        return response



class RoleListView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    ListView,
):
    """
    List all Access Roles.
    """

    permission_required = "auth.view_group"

    model = Group

    template_name = "administration/role_list.html"

    context_object_name = "roles"

    queryset = (
        Group.objects
        .prefetch_related(
            "permissions",
            "user_set",
        )
        .order_by("name")
    )



class RoleDetailView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    DetailView,
):

    permission_required = "auth.view_group"

    model = Group

    template_name = "administration/role_detail.html"

    context_object_name = "role"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["permissions"] = (
            self.object.permissions
            .select_related("content_type")
            .order_by(
                "content_type__app_label",
                "name",
            )
        )

        context["users"] = (
            self.object.user_set
            .filter(is_staff=True)
            .order_by(
                "first_name",
                "last_name",
            )
        )

        return context



class RoleCreateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    TemplateView,
):

    permission_required = "auth.add_group"

    template_name = "administration/coming_soon.html"



class RoleUpdateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    TemplateView,
):

    permission_required = "auth.add_group"

    template_name = "administration/coming_soon.html"