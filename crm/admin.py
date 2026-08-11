from django.contrib import admin
from .models import Lead


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):

    list_display = (
        "reference",
        "full_name",
        "state",
        "status",
        "created_at",
    )

    list_filter = (
        "status",
        "state",
    )

    search_fields = (
        "reference",
        "full_name",
        "email",
        "phone",
    )



from django.contrib import admin
from django.utils.html import format_html

from .models import SalesProfile


@admin.register(SalesProfile)
class SalesProfileAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "referral_code",
        "active",
        "copy_link",
    )

    list_filter = (
        "active",
    )

    search_fields = (
        "user__first_name",
        "user__last_name",
        "user__email",
        "referral_code",
    )

    readonly_fields = (
        "referral_code",
        "created_at",
    )

    def lead_count(self, obj):
        return obj.assessments.count()

    lead_count.short_description = "Assessments"

    def copy_link(self, obj):

        return format_html(
            '<code>/?ref={}</code>',
            obj.referral_code,
        )

    copy_link.short_description = "Referral Link"