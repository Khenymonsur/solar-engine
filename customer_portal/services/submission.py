from django.db import transaction

from audits.models import Assessment, Appliance
from customers.models import Customer
from crm.models import SalesProfile

from customer_portal.services.session import (
    AssessmentSessionService,
)

from .notifications import AssessmentNotificationService


class AssessmentSubmissionService:
    """
    Creates a new assessment for an existing customer.

    This service does NOT create a Django user or Customer profile.
    It simply converts the assessment session into permanent records.
    """

    @classmethod
    @transaction.atomic
    def submit(cls, request, user):

        session = AssessmentSessionService.get(request)

        customer = Customer.objects.get(user=user)

        power_data = session.get("power", {})
        appliances = session.get("appliances", [])


        # ----------------------------------------
        # Determine Assigned Sales Consultant
        # ----------------------------------------

        assigned_sales = None

        sales_profile_id = request.session.get("sales_profile_id")

        if sales_profile_id:
            assigned_sales = SalesProfile.objects.filter(
                pk=sales_profile_id,
                active=True,
            ).first()

        # ----------------------------------------
        # Assessment
        # ----------------------------------------

        assessment = Assessment.objects.create(

            customer=customer,

            assigned_sales=assigned_sales,

            project_name="Customer Portal Assessment",

            backup_hours=power_data.get(
                "backup_hours",
                8,
            ),

            notes="Submitted from Customer Portal.",

            status="Completed",

        )

        # ----------------------------------------
        # Appliances
        # ----------------------------------------

        for item in appliances:

            Appliance.objects.create(

                assessment=assessment,

                appliance_name=item["name"],

                quantity=item["quantity"],

                power_rating=item["watts"],

                hours_per_day=item["hours_per_day"],

            )


        import logging

        logger = logging.getLogger(__name__)

        # --------------------------------------------------
        # Send Notifications
        # --------------------------------------------------

        try:
            AssessmentNotificationService.send_sales_notification(
                request,
                assessment,
            )
        except Exception:
            logger.exception("Failed to send sales notification.")

        try:
            AssessmentNotificationService.send_customer_confirmation(
                request,
                assessment,
            )
        except Exception:
            logger.exception("Failed to send customer confirmation.")

        # --------------------------------------------------
        # Clear Referral Session
        # --------------------------------------------------

        request.session.pop("sales_ref", None)
        request.session.pop("sales_profile_id", None)

        # ----------------------------------------
        # Clear Session
        # ----------------------------------------

        AssessmentSessionService.clear(request)

        return assessment