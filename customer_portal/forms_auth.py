from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import PasswordResetForm

class CustomerLoginForm(AuthenticationForm):
    username = forms.EmailField(
        label="Email Address",
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter your email address",
                "autocomplete": "email",
            }
        ),
    )

    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter your password",
                "autocomplete": "current-password",
            }
        ),
    )



class CustomerPasswordResetForm(PasswordResetForm):
    """
    Password reset form restricted to customer accounts.
    """

    def get_users(self, email):
        """
        Return active users with this email who also
        have a customer profile.
        """

        active_users = super().get_users(email)

        for user in active_users:

            if hasattr(user, "customer_profile"):
                yield user