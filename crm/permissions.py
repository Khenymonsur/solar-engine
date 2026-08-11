from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import redirect


class CRMAccessMixin(PermissionRequiredMixin):
    """
    Base class for CRM permissions.
    """

    permission_required = []

    raise_exception = False

    def handle_no_permission(self):
        messages.error(
            self.request,
            "You do not have permission to access this page."
        )
        return redirect("dashboard:index")