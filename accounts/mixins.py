from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect


class StaffRequiredMixin(UserPassesTestMixin):

    def test_func(self):
        return (
            self.request.user.is_authenticated
            and not hasattr(
                self.request.user,
                "customer_profile",
            )
        )

    def handle_no_permission(self):

        if (
            self.request.user.is_authenticated
            and hasattr(
                self.request.user,
                "customer_profile",
            )
        ):
            return redirect(
                "customer_portal:dashboard"
            )

        return redirect("accounts:login")