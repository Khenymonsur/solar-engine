from core.models import Notification


class NotificationService:

    @staticmethod
    def create(
        *,
        recipient,
        title,
        message="",
        url="",
        notification_type="system",
    ):
        if not recipient:
            return None

        return Notification.objects.create(
            recipient=recipient,
            title=title,
            message=message,
            url=url,
            notification_type=notification_type,
        )