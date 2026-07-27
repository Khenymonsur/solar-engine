from django.contrib import messages
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from .models import (
    Assessment,
    Appliance,
)

from .forms import (
    AssessmentForm,
    ApplianceForm,
)

from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)

from services.recommendation import RecommendationEngine
from services.bom import BillOfMaterialsService

from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)


class AssessmentListView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    ListView,
):
    permission_required = "audits.view_assessment"
    model = Assessment
    template_name = "audits/assessment_list.html"
    context_object_name = "assessments"
    paginate_by = 10

    def get_queryset(self):
        queryset = (
            Assessment.objects
            .select_related("customer")
            .order_by("-created_at")
        )

        search = self.request.GET.get("q")

        if search:
            queryset = queryset.filter(
                Q(project_name__icontains=search)
                | Q(customer__full_name__icontains=search)
                | Q(customer__company_name__icontains=search)
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        assessments = Assessment.objects.all()

        context["assessment_count"] = assessments.count()

        context["draft_count"] = assessments.filter(
            status="Draft"
        ).count()

        context["completed_count"] = assessments.filter(
            status="Completed"
        ).count()

        context["report_count"] = assessments.filter(
            report_generated=True
        ).count()

        return context



class AssessmentDetailView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    DetailView,
):
    permission_required = "audits.view_assessment"
    model = Assessment
    template_name = "audits/assessment_detail.html"
    context_object_name = "assessment"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        assessment = self.object

        items = (
            assessment.appliances
            .select_related("library_appliance")
            .all()
        )

        recommendation = RecommendationEngine(
            assessment
        ).recommend()

        bom = BillOfMaterialsService(
            recommendation
        ).generate()

        context["items"] = items

        context["total_appliances"] = (
            assessment.total_appliances
        )

        context["connected_load"] = (
            assessment.connected_load
        )

        context["peak_load"] = (
            assessment.total_surge_load
        )

        context["daily_energy"] = (
            recommendation["daily_energy"]
        )

        context["critical_load"] = (
            assessment.total_critical_load
        )

        context["recommendation"] = recommendation

        context["bom"] = bom

        return context


class AssessmentCreateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    CreateView,
):
    permission_required = "audits.add_assessment"
    model = Assessment
    form_class = AssessmentForm
    template_name = "audits/assessment_form.html"

    def form_valid(self, form):

        messages.success(
            self.request,
            "Assessment created successfully."
        )

        return super().form_valid(form)

    def get_success_url(self):

        return reverse_lazy(
            "audits:detail",
            kwargs={
                "pk": self.object.pk,
            },
        )


class AssessmentUpdateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UpdateView,
):
    permission_required = "audits.change_assessment"
    model = Assessment
    form_class = AssessmentForm
    template_name = "audits/assessment_form.html"

    def form_valid(self, form):

        messages.success(
            self.request,
            "Assessment updated successfully."
        )

        return super().form_valid(form)

    def get_success_url(self):

        return reverse_lazy(
            "audits:detail",
            kwargs={
                "pk": self.object.pk,
            },
        )


class AssessmentDeleteView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    DeleteView,
):
    permission_required = "audits.delete_assessment"
    model = Assessment
    template_name = "audits/assessment_confirm_delete.html"
    success_url = reverse_lazy("audits:list")

    def delete(self, request, *args, **kwargs):

        messages.success(
            request,
            "Assessment deleted successfully."
        )

        return super().delete(request, *args, **kwargs)


# -----------------------------
# Appliance Views
# -----------------------------

def ApplianceCreateView(request, assessment_id):

    assessment = get_object_or_404(
        Assessment,
        pk=assessment_id,
    )

    if request.method == "POST":

        form = ApplianceForm(request.POST)

        if form.is_valid():

            appliance = form.save(commit=False)

            appliance.assessment = assessment

            appliance.save()

            messages.success(
                request,
                "Appliance added successfully.",
            )

            return redirect(
                "audits:detail",
                pk=assessment.pk,
            )

    else:

        form = ApplianceForm()

    return render(

        request,

        "audits/appliance_form.html",

        {

            "assessment": assessment,

            "form": form,

        },

    )



def ApplianceUpdateView(request, pk):

    appliance = get_object_or_404(
        Appliance,
        pk=pk,
    )

    if request.method == "POST":

        form = ApplianceForm(
            request.POST,
            instance=appliance,
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Appliance updated successfully.",
            )

            return redirect(
                "audits:detail",
                pk=appliance.assessment.pk,
            )

    else:

        form = ApplianceForm(
            instance=appliance,
        )

    return render(

        request,

        "audits/appliance_form.html",

        {

            "assessment": appliance.assessment,

            "form": form,

        },

    )



def ApplianceDeleteView(request, pk):

    appliance = get_object_or_404(
        Appliance,
        pk=pk,
    )

    assessment = appliance.assessment

    if request.method == "POST":

        appliance.delete()

        messages.success(
            request,
            "Appliance deleted.",
        )

        return redirect(
            "audits:detail",
            pk=assessment.pk,
        )

    return render(

        request,

        "audits/appliance_confirm_delete.html",

        {

            "object": appliance,

        },

    )


