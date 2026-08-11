from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from audits.models import Assessment
from .permissions import CRMAccessMixin
from django.views.generic import ListView

from django.views.generic import DetailView



class SalesDashboardView(
    LoginRequiredMixin,
    CRMAccessMixin,
    TemplateView,
):
    permission_required = "crm.view_lead"
    template_name = "crm/dashboard.html"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        profile = self.request.user.sales_profile

        leads = (
            Assessment.objects
            .filter(assigned_sales=profile)
            .select_related("customer")
            .order_by("-created_at")
        )

        context["total_leads"] = leads.count()
        context["recent_leads"] = leads[:5]

        return context




class MyLeadsView(
    LoginRequiredMixin,
    CRMAccessMixin,
    ListView,
):
    permission_required = "crm.view_lead"

    model = Assessment

    template_name = "crm/my_leads.html"

    context_object_name = "leads"

    paginate_by = 20

    def get_queryset(self):

        if not hasattr(self.request.user, "sales_profile"):
            return Assessment.objects.none()

        return (
            Assessment.objects
            .filter(
                assigned_sales=self.request.user.sales_profile
            )
            .select_related(
                "customer",
                "assigned_sales",
            )
            .order_by(
                "-created_at"
            )
        )




class LeadDetailView(
    LoginRequiredMixin,
    CRMAccessMixin,
    DetailView,
):
    permission_required = "crm.view_lead"
    model = Assessment

    template_name = "crm/lead_detail.html"

    context_object_name = "lead"

    def get_queryset(self):

        return (
            Assessment.objects
            .filter(
                assigned_sales=self.request.user.sales_profile
            )
            .select_related(
                "customer",
                "assigned_sales",
            )
        )



