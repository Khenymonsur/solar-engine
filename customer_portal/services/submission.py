from django.db import transaction

from audits.models import Assessment, Appliance
from customers.models import Customer

from customer_portal.services.session import (
    AssessmentSessionService,
)


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
        # Assessment
        # ----------------------------------------

        assessment = Assessment.objects.create(

            customer=customer,

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

        # ----------------------------------------
        # Clear Session
        # ----------------------------------------

        AssessmentSessionService.clear(request)

        return assessment