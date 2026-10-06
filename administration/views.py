from django.contrib.auth import get_user_model

from django.contrib import messages
from django.urls import reverse_lazy

from django.views.generic import (
    CreateView,
    ListView,
    TemplateView,
    UpdateView,
    DetailView,
)

from .forms import (
    StaffUserCreateForm,
    StaffUserForm,
)

from django.db.models import Q
from django.contrib.auth.models import Group, Permission
from django.urls import reverse

from core.mixins import ERPPermissionMixin
from collections import defaultdict
from .forms import StaffRoleForm


from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, redirect
from django.views import View

from django.db.models import Count

User = get_user_model()

class AdministrationDashboardView(
    ERPPermissionMixin,
    TemplateView,
):
    permission_required = "auth.view_user"

    template_name = "administration/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        User = get_user_model()

        context["staff_count"] = User.objects.filter(is_staff=True).count()
        context["active_staff"] = User.objects.filter(
            is_staff=True,
            is_active=True,
        ).count()
        context["inactive_staff"] = User.objects.filter(
            is_staff=True,
            is_active=False,
        ).count()
        context["role_count"] = Group.objects.count()

        return context


class UserListView(
    ERPPermissionMixin,
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

        context["staff_count"] = User.objects.filter(
            is_staff=True
        ).count()

        context["active_staff"] = User.objects.filter(
            is_staff=True,
            is_active=True,
        ).count()

        context["inactive_staff"] = User.objects.filter(
            is_staff=True,
            is_active=False,
        ).count()

        context["role_count"] = Group.objects.count()

        context["user_create_url"] = reverse(
            "administration:user-create"
        )

        return context




class StaffUserUpdateView(
    ERPPermissionMixin,
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
    ERPPermissionMixin,
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



class StaffProfileView(
    ERPPermissionMixin,
    DetailView,
):
    permission_required = "auth.view_user"

    model = User

    template_name = "administration/user_detail.html"

    context_object_name = "staff_user"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.object

        context["roles"] = user.groups.all()

        context["user_list_url"] = reverse(
            "administration:user-list"
        )

        context["user_edit_url"] = reverse(
            "administration:user-edit",
            args=[user.pk],
        )

        context["customer_count"] = (
            user.customer_set.count()
            if hasattr(user, "customer_set")
            else 0
        )

        context["assessment_count"] = (
            user.assessment_set.count()
            if hasattr(user, "assessment_set")
            else 0
        )

        context["quotation_count"] = (
            user.quotation_set.count()
            if hasattr(user, "quotation_set")
            else 0
        )

        context["role_count"] = user.groups.count()

        context["role_form"] = StaffRoleForm(
            instance=self.object
        )

        return context





class RoleListView(
    ERPPermissionMixin,
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
    ERPPermissionMixin,
    DetailView,
):
    """
    Display an Access Role.
    """

    permission_required = "auth.view_group"

    model = Group

    template_name = "administration/role_detail.html"

    context_object_name = "role"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        grouped_permissions = defaultdict(list)

        permissions = (
            self.object.permissions
            .select_related("content_type")
            .order_by(
                "content_type__app_label",
                "codename",
            )
        )

        for permission in permissions:
            app_name = permission.content_type.app_label.replace("_", " ").title()

            grouped_permissions[app_name].append(permission)

        context["grouped_permissions"] = grouped_permissions

        context["permission_count"] = permissions.count()

        context["module_count"] = len(grouped_permissions)

        context["users"] = (
            self.object.user_set
            .filter(is_staff=True)
            .prefetch_related("groups")
            .order_by(
                "first_name",
                "last_name",
            )
        )

        context["user_count"] = context["users"].count()

        return context




class RoleCreateView(
    ERPPermissionMixin,
    TemplateView,
):

    permission_required = "auth.add_group"

    template_name = "administration/coming_soon.html"



class RoleUpdateView(
    ERPPermissionMixin,
    TemplateView,
):

    permission_required = "auth.add_group"

    template_name = "administration/coming_soon.html"






class StaffRoleUpdateView(
    ERPPermissionMixin,
    View,
):
    permission_required = "auth.change_user"

    def post(self, request, pk):

        user = get_object_or_404(User, pk=pk)

        form = StaffRoleForm(
            request.POST,
            instance=user,
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Access roles updated successfully."
            )

        return redirect(
            "administration:user-detail",
            pk=pk,
        )




class StaffAccountStatusView(
    ERPPermissionMixin,
    View,
):
    permission_required = "auth.change_user"

    def post(self, request, pk):

        user = get_object_or_404(
            User,
            pk=pk,
        )

        # Prevent disabling yourself
        if user == request.user:

            messages.error(
                request,
                "You cannot disable your own account."
            )

            return redirect(
                "administration:user-detail",
                pk=pk,
            )

        user.is_active = not user.is_active

        user.save(
            update_fields=["is_active"]
        )

        if user.is_active:

            messages.success(
                request,
                f"{user.get_full_name() or user.username} has been enabled."
            )

        else:

            messages.success(
                request,
                f"{user.get_full_name() or user.username} has been disabled."
            )

        return redirect(
            "administration:user-detail",
            pk=pk,
        )