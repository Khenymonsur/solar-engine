from django.urls import path
from django.views.generic import RedirectView

from . import views

app_name = "customer_portal"

# urlpatterns = [
#
#     path(
#         "",
#         views.CustomerDashboardView.as_view(),
#         name="dashboard",
#     ),

urlpatterns = [

    path(
        "",
        RedirectView.as_view(
            pattern_name="customer_portal:login",
            permanent=False,
        ),
    ),

    path(
        "dashboard/",
        views.CustomerDashboardView.as_view(),
        name="dashboard",
    ),


# Authentication
    path("register/",
         views.CustomerRegisterView.as_view(),
         name="register"
    ),

    path("login/",
         views.CustomerLoginView.as_view(),
         name="login"
    ),

    path("logout/",
         views.customer_logout,
         name="logout"
    ),

    path("forgot-password/",
         views.ForgotPasswordView.as_view(),
         name="forgot_password"
    ),


# Assessment Wizard

    path(
            "assessment/new/",
            views.NewAssessmentView.as_view(),
            name="new-assessment",
        ),

    path(
        "assessment/",
        views.AssessmentStepOneView.as_view(),
        name="assessment_step1",
    ),

    path(
        "assessment/property/",
        views.AssessmentStepTwoView.as_view(),
        name="assessment_step2",
    ),

    path(
        "assessment/power/",
        views.AssessmentStepThreeView.as_view(),
        name="assessment_step3",
    ),

    path(
        "assessment/appliances/",
        views.AssessmentStepFourView.as_view(),
        name="assessment_step4",
    ),

    path(
        "assessment/appliances/add/",
        views.AddApplianceView.as_view(),
        name="add_appliance",
    ),

    path(
        "assessment/appliances/remove/<int:appliance_id>/",
        views.RemoveApplianceView.as_view(),
        name="remove_appliance",
    ),

    path(
        "assessment/preview/",
        views.AssessmentPreviewView.as_view(),
        name="assessment_preview",
    ),

    path(
        "assessment/<int:pk>/",
        views.CustomerAssessmentDetailView.as_view(),
        name="assessment-detail",
    ),

    path(
        "assessment/submit/",
        views.SubmitAssessmentView.as_view(),
        name="submit-assessment",
    ),

    path(
        "keep-alive/",
        views.keep_alive,
        name="keep_alive",
    ),


]