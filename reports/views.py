from django.views.generic import ListView
from django.views.generic import DetailView

from audits.models import Assessment
from services.recommendation import RecommendationEngine
from services.bom import BillOfMaterialsService

from django.http import HttpResponse
from django.template.loader import render_to_string

from weasyprint import HTML

from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)



class ReportListView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    ListView,
):
    permission_required = "audits.view_assessment"
    model = Assessment
    template_name = "reports/report_list.html"
    context_object_name = "reports"
    paginate_by = 15
    queryset = (
        Assessment.objects
        .select_related("customer")
        .order_by("-created_at")
    )



class ReportDetailView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    DetailView,
):
    permission_required = "audits.view_assessment"
    model = Assessment
    template_name = "reports/report_detail.html"
    context_object_name = "assessment"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        recommendation = (
            RecommendationEngine(
                self.object
            ).recommend()
        )

        bom = (
            BillOfMaterialsService(
                recommendation
            ).generate()
        )

        context["recommendation"] = recommendation

        context["bom"] = bom
        context["report_number"] = (
            f"CEPL-"
            f"{self.object.created_at.year}-"
            f"{self.object.pk:05d}"
        )

        return context



class ReportPDFView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    DetailView,
):
    permission_required = "audits.view_assessment"
    model = Assessment
    template_name = "reports/report_detail.html"
    context_object_name = "assessment"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        recommendation = RecommendationEngine(
            self.object
        ).recommend()

        bom = BillOfMaterialsService(
            recommendation
        ).generate()

        context["recommendation"] = recommendation
        context["bom"] = bom

        context["report_number"] = (
            f"CEPL/PV/"
            f"{self.object.created_at.year}/"
            f"{self.object.pk:05d}"
        )

        return context

    def get(self, request, *args, **kwargs):

        self.object = self.get_object()

        context = self.get_context_data()

        html = render_to_string(
            self.template_name,
            context,
            request=request,
        )

        pdf = HTML(
            string=html,
            base_url=request.build_absolute_uri("/")
        ).write_pdf()

        response = HttpResponse(
            pdf,
            content_type="application/pdf",
        )

        response["Content-Disposition"] = (
            f'inline; filename="{context["report_number"]}.pdf"'
        )

        return response
