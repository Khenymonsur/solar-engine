from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (
    FormView,
    TemplateView,
)

from .forms import (
    CustomerRegistrationForm,
    AssessmentStepOneForm,
    AssessmentStepTwoForm,
    AssessmentStepThreeForm,
    AssessmentApplianceForm,
)

from customer_portal.services.session import (
    AssessmentSessionService,
)
from customer_portal.services.estimation import CustomerEstimationService

from django.shortcuts import redirect

from django.contrib.auth import login, logout
from django.contrib import messages

from django.contrib.auth.views import LoginView
from customer_portal.services.registration import RegistrationService


from django.views.generic import DetailView
from audits.models import Assessment
from django.contrib.auth.mixins import LoginRequiredMixin
from customers.models import Customer

from customer_portal.forms_auth import CustomerLoginForm



# ----------------------------------------------------------
# Customer Registration
# ----------------------------------------------------------

class CustomerRegisterView(FormView):

    template_name = "customer_portal/auth/register.html"

    form_class = CustomerRegistrationForm

    success_url = reverse_lazy(
        "customer_portal:dashboard"
    )

    def dispatch(self, request, *args, **kwargs):

        assessment = AssessmentSessionService.get(request)

        if "customer" not in assessment:

            return redirect(
                "customer_portal:assessment_step1"
            )

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        assessment = AssessmentSessionService.get(self.request)

        context["customer"] = assessment.get(
            "customer",
            {},
        )

        return context

    def form_valid(self, form):

        assessment = AssessmentSessionService.get(
            self.request
        )

        customer = assessment["customer"]

        names = customer["full_name"].split()

        first_name = names[0]

        last_name = " ".join(names[1:]) if len(names) > 1 else ""

        if User.objects.filter(
                username=customer["email"]
        ).exists():
            messages.error(

                self.request,

                "An account with this email already exists."

            )

            return redirect(
                "customer_portal:login"
            )

        user = User.objects.create_user(

            username=customer["email"],

            email=customer["email"],

            first_name=first_name,

            last_name=last_name,

            password=form.cleaned_data["password1"],

        )

        login(
            self.request,
            user,
        )

        assessment = RegistrationService.complete_registration(
            self.request,
            user,
        )

        messages.success(

            self.request,

            "Welcome to Cloud Energy!",

        )

        return redirect(
            "customer_portal:assessment-detail",
            pk=assessment.pk,
        )

# ----------------------------------------------------------
# Login
# ----------------------------------------------------------

# class CustomerLoginView(LoginView):
#     template_name = "customer_portal/auth/login.html"
#     redirect_authenticated_user = True
#
#     def get_success_url(self):
#         return reverse_lazy(
#             "customer_portal:dashboard"
#         )


from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.urls import reverse


class CustomerLoginView(LoginView):
    template_name = "customer_portal/auth/login.html"
    redirect_authenticated_user = True

    def form_valid(self, form):
        login(self.request, form.get_user())

        print("CUSTOMER LOGIN SUCCESS")

        return HttpResponseRedirect(
            reverse("customer_portal:dashboard")
        )


# class CustomerLoginView(LoginView):
#
#     template_name = "customer_portal/auth/login.html"
#
#     authentication_form = CustomerLoginForm
#
#     redirect_authenticated_user = True
#
#     def get_success_url(self):
#         return reverse_lazy("customer_portal:dashboard")

# ----------------------------------------------------------
# Logout
# ----------------------------------------------------------
def customer_logout(request):

    logout(request)

    messages.success(
        request,
        "You have been logged out successfully."
    )

    return redirect(
        "customer_portal:login"
    )

# ----------------------------------------------------------
# Forget Password
# ----------------------------------------------------------
class ForgotPasswordView(TemplateView):

    template_name = (
        "customer_portal/auth/forgot_password.html"
    )





# ----------------------------------------------------------
# Dashboard
# ----------------------------------------------------------

class CustomerDashboardView(LoginRequiredMixin, TemplateView):

    template_name = "customer_portal/dashboard.html"

    login_url = "customer_portal:login"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        customer = Customer.objects.filter(
            user=self.request.user
        ).first()

        assessment = None

        if customer:

            assessment = (
                Assessment.objects
                .filter(customer=customer)
                .order_by("-created_at")
                .first()
            )

        context["customer"] = customer
        context["assessment"] = assessment

        return context


# ----------------------------------------------------------
# Step 1
# ----------------------------------------------------------

class AssessmentStepOneView(FormView):

    template_name = "customer_portal/assessment/step1.html"

    form_class = AssessmentStepOneForm

    def form_valid(self, form):

        AssessmentSessionService.save_customer(

            self.request,

            form.cleaned_data,

        )

        return redirect(
            "customer_portal:assessment_step2"
        )


# ----------------------------------------------------------
# Step 2
# ----------------------------------------------------------

class AssessmentStepTwoView(FormView):

    template_name = "customer_portal/assessment/step2.html"

    form_class = AssessmentStepTwoForm

    def dispatch(self, request, *args, **kwargs):

        assessment = AssessmentSessionService.get(
            request
        )

        if "customer" not in assessment:

            return redirect(
                "customer_portal:assessment_step1"
            )

        return super().dispatch(
            request,
            *args,
            **kwargs,
        )

    def form_valid(self, form):

        AssessmentSessionService.save_property(

            self.request,

            form.cleaned_data,

        )

        return redirect(
            "customer_portal:assessment_step3"
        )



# ----------------------------------------------------------
# Step 3
# ----------------------------------------------------------

class AssessmentStepThreeView(FormView):

    template_name = "customer_portal/assessment/step3.html"

    form_class = AssessmentStepThreeForm

    def dispatch(self, request, *args, **kwargs):

        assessment = AssessmentSessionService.get(
            request
        )

        if "property" not in assessment:

            return redirect(
                "customer_portal:assessment_step2"
            )

        return super().dispatch(
            request,
            *args,
            **kwargs,
        )

    def form_valid(self, form):

        AssessmentSessionService.save_power(

            self.request,

            form.cleaned_data,

        )

        return redirect(
            "customer_portal:assessment_step4"
        )


# ----------------------------------------------------------
# Step 4
# ----------------------------------------------------------

class AssessmentStepFourView(TemplateView):

    template_name = (
        "customer_portal/assessment/step4.html"
    )

    def dispatch(self, request, *args, **kwargs):

        assessment = AssessmentSessionService.get(
            request
        )

        if "power" not in assessment:

            return redirect(
                "customer_portal:assessment_step3"
            )

        return super().dispatch(
            request,
            *args,
            **kwargs,
        )

    def get_context_data(self, **kwargs):

        context = super().get_context_data(
            **kwargs
        )

        context["form"] = AssessmentApplianceForm()

        context["appliances"] = (

            AssessmentSessionService.selected_appliances(
                self.request
            )

        )

        context["connected_load"] = (

            AssessmentSessionService.connected_load(
                self.request
            )

        )

        context["appliance_count"] = (

            AssessmentSessionService.appliance_count(
                self.request
            )

        )

        context["daily_energy"] = (
            AssessmentSessionService.daily_energy(
                self.request
            )
        )

        return context


# ----------------------------------------------------------
# Add Appliance
# ----------------------------------------------------------

class AddApplianceView(View):

    def post(self, request):

        form = AssessmentApplianceForm(
            request.POST
        )

        if form.is_valid():
            AssessmentSessionService.add_appliance(

                request,

                form.cleaned_data["appliance_name"],
                form.cleaned_data["watts"],
                form.cleaned_data["quantity"],
                form.cleaned_data["hours_per_day"],

            )

        return redirect(
            "customer_portal:assessment_step4"
        )


# ----------------------------------------------------------
# Remove Appliance
# ----------------------------------------------------------

class RemoveApplianceView(View):

    def post(
        self,
        request,
        appliance_id,
    ):

        AssessmentSessionService.remove_appliance(

            request,

            appliance_id,

        )

        return redirect(
            "customer_portal:assessment_step4"
        )



class AssessmentPreviewView(TemplateView):

    template_name = (
        "customer_portal/assessment/preview.html"
    )

    def dispatch(self, request, *args, **kwargs):

        assessment = AssessmentSessionService.get(request)

        if not assessment.get("appliances"):
            return redirect(
                "customer_portal:assessment_step4"
            )

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        estimate = CustomerEstimationService(
            self.request
        )

        context["estimate"] = estimate.summary()

        context["assessment"] = (
            AssessmentSessionService.get(
                self.request
            )
        )

        return context



class CustomerAssessmentDetailView(
    LoginRequiredMixin,
    DetailView,
):
    model = Assessment

    template_name = (
        "customer_portal/assessment/customer_assessment.html"
    )

    context_object_name = "assessment"

    def get_queryset(self):

        return Assessment.objects.filter(
            customer__user=self.request.user
        )

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


@login_required
def keep_alive(request):
    return JsonResponse({"status": "ok"})