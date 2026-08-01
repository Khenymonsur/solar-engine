from django.db import transaction
from customers.models import Customer

from customer_portal.services import AssessmentSessionService
from customer_portal.services.submission import (
    AssessmentSubmissionService,
)


class RegistrationService:
    """
    Converts a completed Customer Portal assessment
    into permanent database records.
    """

    @classmethod
    @transaction.atomic
    def complete_registration(cls, request, user):
        """
        Creates:
            - Customer
            - Assessment
            - Assessment Appliances

        Returns:
            Assessment instance
        """

        session = AssessmentSessionService.get(request)

        customer_data = session.get("customer", {})
        property_data = session.get("property", {})
        power_data = session.get("power", {})
        appliances = session.get("appliances", [])

        # ----------------------------------------
        # Customer
        # ----------------------------------------

        customer, created = Customer.objects.update_or_create(

            user=user,

            defaults={

                "full_name": customer_data["full_name"],

                "phone": customer_data["phone"],

                "whatsapp": customer_data.get(
                    "whatsapp",
                    "",
                ),

                "address": property_data["address"],

                "state": property_data["state"],

                "lga": property_data.get(
                    "lga",
                    "",
                ),

                "building_type": property_data.get(
                    "building_type",
                    Customer.RESIDENTIAL,
                ),

            },

        )

        # ----------------------------------------
        # Assessment
        # ----------------------------------------

        assessment = AssessmentSubmissionService.submit(
            request,
            user,
        )

        return assessment