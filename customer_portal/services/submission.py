from django.db import transaction

from audits.models import Assessment, Appliance
from customers.models import Customer
from crm.models import SalesProfile

from customer_portal.services.session import (
    AssessmentSessionService,
)

from .notifications import AssessmentNotificationService
from django.urls import reverse
from core.services.notifications import NotificationService




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

            backup_hours=power_data.get("backup_hours", 8),

            grid_available=(
                    power_data.get("grid_available") == "yes"
            ),

            generator_available=(
                    power_data.get("generator_available") == "yes"
            ),

            has_existing_solar=(
                    power_data.get("has_existing_solar") == "yes"
            ),

            has_existing_inverter=(
                    power_data.get("has_existing_inverter") == "yes"
            ),

            has_existing_battery=(
                    power_data.get("has_existing_battery") == "yes"
            ),

            generator_capacity=power_data.get(
                "generator_capacity"
            ) or None,

            existing_inverter_capacity=power_data.get(
                "existing_inverter_capacity"
            ) or None,

            existing_battery_capacity=power_data.get(
                "existing_battery_capacity"
            ) or None,

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

        # --------------------------------------------------
        # Send Notifications After Successful DB Commit
        # --------------------------------------------------

        def send_notifications():

            import logging

            logger = logging.getLogger(__name__)

            # --------------------------------------------------
            # Create In-App Notification For Assigned Sales
            # --------------------------------------------------

            if assessment.assigned_sales:

                sales_user = assessment.assigned_sales.user

                try:
                    NotificationService.create(
                        recipient=sales_user,
                        notification_type="assessment",
                        title="New Solar Assessment",
                        message=(
                            f"{assessment.customer.full_name} submitted "
                            f"assessment {assessment.reference}."
                        ),
                        url=reverse(
                            "audits:detail",
                            kwargs={"pk": assessment.pk},
                        ),
                    )

                except Exception:
                    logger.exception(
                        "Failed to create in-app notification "
                        "for assessment %s.",
                        assessment.reference,
                    )

            try:
                AssessmentNotificationService.send_sales_notification(
                    request,
                    assessment,
                )
            except Exception:
                logger.exception(
                    "Failed to send sales notification "
                    "for assessment %s.",
                    assessment.reference,
                )
            # --------------------------------------------------
            # Send Customer Confirmation Email
            # --------------------------------------------------

            try:
                AssessmentNotificationService.send_customer_confirmation(
                    request,
                    assessment,
                )
            except Exception:
                logger.exception(
                    "Failed to send customer confirmation "
                    "for assessment %s.",
                    assessment.reference,
                )

        transaction.on_commit(
            send_notifications
        )

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