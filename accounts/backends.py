from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend


User = get_user_model()


class EmailBackend(BaseBackend):

    def authenticate(
        self,
        request,
        username=None,
        password=None,
        **kwargs,
    ):
        """
        Authenticate customer users by email.

        Only users linked to a Customer profile are considered.
        This prevents conflicts when a staff account uses
        the same email address.
        """

        email = (
            kwargs.get("email")
            or username
        )

        if not email or not password:
            return None

        users = (
            User.objects
            .filter(
                email__iexact=email,
                is_active=True,
                customer_profile__isnull=False,
            )
            .distinct()
        )

        for user in users:

            if user.check_password(password):
                return user

        return None


    def get_user(self, user_id):

        try:
            return User.objects.get(
                pk=user_id,
            )

        except User.DoesNotExist:
            return None