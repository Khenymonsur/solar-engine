from django.views.generic import TemplateView
from django.shortcuts import redirect


class HomeView(TemplateView):

    template_name = "website/home.html"

    def dispatch(self, request, *args, **kwargs):

        # ---------------------------------------
        # Referral Link
        # ---------------------------------------

        if request.GET.get("ref"):

            # ReferralMiddleware has already validated
            # and stored the referral in the session.
            return redirect("customer_portal:assessment_step1")

        # ---------------------------------------
        # Logged-in users
        # ---------------------------------------

        if request.user.is_authenticated:

            # Staff and Superusers
            if request.user.is_staff or request.user.is_superuser:
                return redirect("dashboard:index")

            # Customer
            return redirect("customer_portal:dashboard")

        return super().dispatch(request, *args, **kwargs)


class AboutView(TemplateView):

    template_name = "website/about.html"


class ServicesView(TemplateView):

    template_name = "website/services.html"


class ContactView(TemplateView):

    template_name = "website/contact.html"