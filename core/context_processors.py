from django.conf import settings

def google_maps(request):
    return {
        "GOOGLE_MAPS_API_KEY": settings.GOOGLE_MAPS_API_KEY
    }


def session_timeout(request):
    return {
        "SESSION_TIMEOUT": settings.SESSION_TIMEOUT,
        "SESSION_WARNING_TIME": settings.SESSION_WARNING_TIME,
    }


from crm.models import SalesProfile


def staff_context(request):
    """
    Provides the current staff role to all templates.
    """

    role = None

    if request.user.is_authenticated:

        if request.user.is_superuser:
            role = "admin"

        elif SalesProfile.objects.filter(
            user=request.user,
            active=True
        ).exists():
            role = "sales"

        elif request.user.groups.filter(
            name="Engineer"
        ).exists():
            role = "engineer"

        elif request.user.groups.filter(
            name="Finance"
        ).exists():
            role = "finance"

        else:
            role = "staff"

    return {
        "staff_role": role,
    }