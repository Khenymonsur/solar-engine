from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from customers.models import Customer
from audits.models import Assessment
from equipment.models import (
    Battery,
    Inverter,
    SolarPanel,
    ChargeController,
)

from django.utils import timezone


from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import UpdateView, TemplateView

from .forms import (
    ProfileForm,
    PreferenceForm,
    SystemSettingForm,
)

from .models import (
    UserProfile,
    UserPreference,
    SystemSetting,
)


from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)



@login_required(login_url="accounts:login")
def dashboard(request):

    equipment_count = (
        Battery.objects.count()
        + Inverter.objects.count()
        + SolarPanel.objects.count()
        + ChargeController.objects.count()
    )

    context = {
        "customer_count": Customer.objects.count(),
        "assessment_count": Assessment.objects.count(),
        "equipment_count": equipment_count,
        "report_count": 0,
        "recent_assessments": Assessment.objects.order_by("-created_at")[:10],
        "now": timezone.now(),
    }

    return render(
        request,
        "dashboard/index.html",
        context,
    )


class ProfileView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UpdateView,
):
    permission_required = "dashboard.view_userprofile"
    raise_exception = True
    model = UserProfile
    form_class = ProfileForm
    template_name = "dashboard/profile.html"
    success_url = reverse_lazy("dashboard:profile")

    def get_object(self):

        profile, created = UserProfile.objects.get_or_create(
            user=self.request.user
        )

        return profile

    def form_valid(self, form):

        messages.success(
            self.request,
            "Profile updated successfully."
        )

        return super().form_valid(form)



class PreferenceView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UpdateView,
):
    permission_required = "dashboard.view_userpreference"
    raise_exception = True
    model = UserPreference
    form_class = PreferenceForm
    template_name = "dashboard/preferences.html"
    success_url = reverse_lazy("dashboard:preferences")

    def get_object(self):

        preference, created = UserPreference.objects.get_or_create(
            user=self.request.user
        )

        return preference

    def form_valid(self, form):

        messages.success(
            self.request,
            "Preferences saved successfully."
        )

        return super().form_valid(form)




class AnalyticsView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    TemplateView,
):
    permission_required = "dashboard.view_analytics"
    raise_exception = True
    template_name = "dashboard/analytics.html"




class SettingsView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UpdateView
):

    permission_required = "dashboard.manage_system_settings"
    raise_exception = True
    model = SystemSetting
    form_class = SystemSettingForm
    template_name = "dashboard/settings.html"
    success_url = reverse_lazy("dashboard:settings")

    def get_object(self):

        settings, created = SystemSetting.objects.get_or_create(
            pk=1
        )

        return settings

    def form_valid(self, form):

        messages.success(
            self.request,
            "System settings updated successfully.",
        )

        return super().form_valid(form)