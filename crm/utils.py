from crm.models import SalesProfile


def user_role(user):
    """
    Determine the staff role for the current user.
    """

    if not user.is_authenticated:
        return None

    if user.is_superuser:
        return "admin"

    if hasattr(user, "sales_profile"):
        return "sales"

    if user.groups.filter(name="Engineer").exists():
        return "engineer"

    if user.groups.filter(name="Finance").exists():
        return "finance"

    return "staff"