from django.conf import settings
from core.models import Notification




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

    role = None
    staff_notifications = []
    unread_notification_count = 0

    if request.user.is_authenticated:

        if request.user.is_superuser:
            role = "admin"

        elif SalesProfile.objects.filter(
            user=request.user,
            active=True,
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

        staff_notifications = (
            Notification.objects
            .filter(recipient=request.user)
            .order_by("-created_at")[:6]
        )

        unread_notification_count = (
            Notification.objects
            .filter(
                recipient=request.user,
                is_read=False,
            )
            .count()
        )

    return {
        "staff_role": role,
        "staff_notifications": staff_notifications,
        "unread_notification_count": unread_notification_count,
    }