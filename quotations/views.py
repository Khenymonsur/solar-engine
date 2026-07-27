from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import QuotationForm
from .models import Quotation


from django.shortcuts import get_object_or_404, redirect
from django.views import View

from django.db.models import Sum
from audits.models import Assessment
from .services import QuotationService

from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)




class QuotationListView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    ListView,
):
    permission_required = "quotations.view_quotation"
    model = Quotation
    template_name = "quotations/quotation_list.html"
    context_object_name = "quotations"
    paginate_by = 20

    from django.db.models import Sum

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        quotations = Quotation.objects.all()

        context.update({

            "quotation_count": quotations.count(),

            "draft_count": quotations.filter(
                status="draft"
            ).count(),

            "sent_count": quotations.filter(
                status="sent"
            ).count(),

            "accepted_count": quotations.filter(
                status="accepted"
            ).count(),

            "total_value": quotations.aggregate(
                total=Sum("grand_total")
            )["total"] or 0,

        })

        return context


class QuotationDetailView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    DetailView,
):
    permission_required = "quotations.view_quotation"
    model = Quotation
    template_name = "quotations/quotation_detail.html"
    context_object_name = "quotation"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["items"] = self.object.items.all()

        return context


class QuotationCreateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    CreateView,
):
    permission_required = "quotations.add_quotation"
    model = Quotation
    form_class = QuotationForm
    template_name = "quotations/quotation_form.html"
    success_url = reverse_lazy("quotations:list")

    def form_valid(self, form):
        messages.success(
            self.request,
            "Quotation created successfully."
        )
        return super().form_valid(form)


class QuotationUpdateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UpdateView,
):
    permission_required = "quotations.change_quotation"
    model = Quotation
    form_class = QuotationForm
    template_name = "quotations/quotation_form.html"
    success_url = reverse_lazy("quotations:list")

    def form_valid(self, form):
        messages.success(
            self.request,
            "Quotation updated successfully."
        )
        return super().form_valid(form)


class QuotationDeleteView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    DeleteView,
):
    permission_required = "quotations.delete_quotation"
    model = Quotation
    template_name = "quotations/quotation_confirm_delete.html"
    context_object_name = "quotation"
    success_url = reverse_lazy("quotations:list")

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Quotation deleted successfully.")
        return super().delete(request, *args, **kwargs)


class GenerateQuotationView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    View,
):
    permission_required = "quotations.change_quotation"

    def get(self, request, assessment_id):

        assessment = get_object_or_404(
            Assessment,
            pk=assessment_id,
        )

        # Prevent duplicate quotations
        existing = Quotation.objects.filter(
            assessment=assessment
        ).first()

        if existing:

            messages.info(
                request,
                "A quotation already exists for this assessment."
            )

            return redirect(
                "quotations:detail",
                pk=existing.pk,
            )

        quotation = QuotationService.create_from_assessment(
            assessment
        )

        messages.success(
            request,
            "Quotation generated successfully."
        )

        return redirect(
            "quotations:detail",
            pk=quotation.pk,
        )




