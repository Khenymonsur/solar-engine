from datetime import timedelta

from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.utils import timezone


class SessionTimeoutMiddleware:
    """
    Automatically logs out inactive users.

    Activity is any HTTP request.
    """

    def __init__(self, get_response):
        self.get_response = get_response

        # 2 minutes for testing
        self.timeout = timedelta(seconds=3)

    def __call__(self, request):

        if request.user.is_authenticated:

            now = timezone.now()

            last_activity = request.session.get(
                "last_activity"
            )

            if last_activity:

                last_activity = timezone.datetime.fromisoformat(
                    last_activity
                )

                if now - last_activity > self.timeout:

                    logout(request)

                    if request.path.startswith("/portal/"):

                        return redirect(
                            "customer_portal:login"
                        )

                    return redirect(
                        "accounts:login"
                    )

            request.session["last_activity"] = (
                now.isoformat()
            )

        return self.get_response(request)