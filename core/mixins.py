from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)


class ERPPermissionMixin(
    LoginRequiredMixin,
    PermissionRequiredMixin,
):
    """
    Base mixin used throughout the ERP.

    Ensures:
    - user is authenticated
    - required permission is checked
    - permission errors return 403
    """

    raise_exception = True