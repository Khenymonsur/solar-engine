from django.contrib import admin

from .models import (
    UserProfile,
    UserPreference,
    SystemSetting,
)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "department",
        "employee_id",
        "job_title",
    )

    search_fields = (
        "user__username",
        "department",
    )


@admin.register(UserPreference)
class UserPreferenceAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "theme",
        "language",
        "timezone",
    )


@admin.register(SystemSetting)
class SystemSettingAdmin(admin.ModelAdmin):

    list_display = (
        "company_name",
        "currency",
        "updated_at",
    )