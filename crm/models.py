from django.conf import settings
from django.db import models


class Lead(models.Model):

    STATUS_CHOICES = [
        ("new", "New"),
        ("contacted", "Contacted"),
        ("qualified", "Qualified"),
        ("proposal", "Proposal Sent"),
        ("won", "Won"),
        ("lost", "Lost"),
    ]

    reference = models.CharField(
        max_length=20,
        unique=True,
    )

    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="leads",
    )

    full_name = models.CharField(max_length=200)

    email = models.EmailField()

    phone = models.CharField(max_length=20)

    property_type = models.CharField(max_length=50)

    state = models.CharField(max_length=100)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="new",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return f"{self.reference} - {self.full_name}"




import secrets

class SalesProfile(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sales_profile",
    )

    referral_code = models.CharField(
        max_length=20,
        unique=True,
        editable=False,
    )

    phone = models.CharField(
        max_length=20,
        blank=True,
    )

    active = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def save(self, *args, **kwargs):

        if not self.referral_code:

            self.referral_code = (
                "SAL-" +
                secrets.token_hex(3).upper()
            )

        super().save(*args, **kwargs)

    @property
    def referral_link(self):

        return (
            f"/?ref={self.referral_code}"
        )

    def __str__(self):

        return (
            f"{self.user.get_full_name()} "
            f"({self.referral_code})"
        )