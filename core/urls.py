from . import views
from django.urls import path

app_name = "core"

urlpatterns = [

    path(
        "notifications/",
        views.notification_list,
        name="notifications",
    ),

    path(
        "notifications/<int:pk>/open/",
        views.notification_open,
        name="notification-open",
    ),

    path(
        "notifications/mark-all-read/",
        views.mark_all_notifications_read,
        name="notifications-mark-all-read",
    ),

]