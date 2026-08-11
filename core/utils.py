from crm.models import SalesProfile


def get_staff_role(user):

    if not user.is_authenticated:
        return None

    if user.is_superuser:
        return "admin"

    if SalesProfile.objects.filter(
        user=user,
        active=True
    ).exists():
        return "sales"

    if user.groups.filter(
        name="Engineer"
    ).exists():
        return "engineer"

    if user.groups.filter(
        name="Finance"
    ).exists():
        return "finance"

    return "staff"