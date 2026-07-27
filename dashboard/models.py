from django.conf import settings
from django.db import models


class UserProfile(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )

    avatar = models.ImageField(
        upload_to="profiles/",
        blank=True,
        null=True,
    )

    phone = models.CharField(
        max_length=20,
        blank=True,
    )

    department = models.CharField(
        max_length=100,
        blank=True,
    )

    employee_id = models.CharField(
        max_length=50,
        blank=True,
    )

    job_title = models.CharField(
        max_length=100,
        blank=True,
    )

    biography = models.TextField(
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return self.user.get_full_name() or self.user.username





class UserPreference(models.Model):

    THEME_CHOICES = [

        ("light", "Light"),

        ("dark", "Dark"),

        ("system", "System"),
    ]

    DATE_FORMATS = [

        ("dd/mm/yyyy", "DD/MM/YYYY"),

        ("mm/dd/yyyy", "MM/DD/YYYY"),

        ("yyyy-mm-dd", "YYYY-MM-DD"),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="preferences",
    )

    theme = models.CharField(
        max_length=20,
        choices=THEME_CHOICES,
        default="light",
    )

    email_notifications = models.BooleanField(
        default=True,
    )

    browser_notifications = models.BooleanField(
        default=True,
    )

    assessment_alerts = models.BooleanField(
        default=True,
    )

    customer_alerts = models.BooleanField(
        default=True,
    )

    weekly_summary = models.BooleanField(
        default=False,
    )

    show_dashboard_stats = models.BooleanField(
        default=True,
    )

    show_recent_assessments = models.BooleanField(
        default=True,
    )

    show_recent_customers = models.BooleanField(
        default=True,
    )

    show_quick_actions = models.BooleanField(
        default=True,
    )

    language = models.CharField(
        max_length=50,
        default="English",
    )

    timezone = models.CharField(
        max_length=100,
        default="Africa/Lagos",
    )

    date_format = models.CharField(
        max_length=20,
        choices=DATE_FORMATS,
        default="dd/mm/yyyy",
    )

    def __str__(self):
        return f"{self.user.username} Preferences"




class SystemSetting(models.Model):

    company_name = models.CharField(
        max_length=200,
        default="Cloud Energy Photoelectric Ltd",
    )

    company_email = models.EmailField(
        blank=True,
    )

    company_phone = models.CharField(
        max_length=30,
        blank=True,
    )

    website = models.URLField(
        blank=True,
    )

    company_logo = models.ImageField(
        upload_to="company/",
        blank=True,
        null=True,
    )

    currency = models.CharField(
        max_length=10,
        default="NGN",
    )

    quotation_prefix = models.CharField(
        max_length=10,
        default="QT-",
    )

    invoice_prefix = models.CharField(
        max_length=10,
        default="INV-",
    )

    default_backup_hours = models.PositiveIntegerField(
        default=8,
    )

    safety_margin = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=25,
    )

    default_voltage = models.PositiveIntegerField(
        default=230,
    )

    email_notifications = models.BooleanField(
        default=True,
    )

    google_maps_api_key = models.CharField(
        max_length=255,
        blank=True,
    )

    weather_api_key = models.CharField(
        max_length=255,
        blank=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        verbose_name = "System Setting"

        verbose_name_plural = "System Settings"

        permissions = [

            ("view_analytics", "Can view analytics"),

            ("manage_system_settings", "Can manage system settings"),

        ]

    def __str__(self):
        return "System Settings"
