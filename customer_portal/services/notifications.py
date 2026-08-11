from django.urls import reverse
from .email import EmailService


class AssessmentNotificationService:
    """
    Handles all notifications related to customer assessments.
    """

    @staticmethod
    def send_sales_notification(request, assessment):
        """
        Notify the assigned salesperson about a new assessment.
        """

        sales_profile = assessment.assigned_sales

        if not sales_profile:
            return False

        sales_user = sales_profile.user

        if not sales_user.email:
            return False

        customer = assessment.customer

        assessment_url = request.build_absolute_uri(
            reverse(
                "audits:detail",
                kwargs={"pk": assessment.pk},
            )
        )

        subject = (
            f"New Solar Assessment Assigned - "
            f"{customer.full_name}"
        )

        message = f"""
Hello {sales_user.get_full_name() or sales_user.username},

A new customer has completed a solar assessment.

Customer Details
----------------
Name: {customer.full_name}
Email: {customer.email}
Phone: {customer.phone}

Assessment
----------
Project: {assessment.project_name}

View Assessment
---------------
{assessment_url}

Please log into the Staff Portal and follow up with this customer.

Regards,

Cloud Energy Photoelectric Ltd
"""

        EmailService.send(
            subject=subject,
            recipients=[sales_user.email],
            message=message,
        )

        return True

    @staticmethod
    def send_customer_confirmation(request, assessment):
        """
        Send a confirmation email to the customer.
        """

        customer = assessment.customer

        if not customer.email:
            return False

        consultant = "Our Sales Team"

        if assessment.assigned_sales:

            sales_user = assessment.assigned_sales.user

            consultant = (
                sales_user.get_full_name()
                or sales_user.username
            )

        subject = "Your Solar Assessment Has Been Received"

        message = f"""
Dear {customer.full_name},

Thank you for completing your solar assessment with
Cloud Energy Photoelectric Ltd.

We have successfully received your assessment.

Assigned Consultant
-------------------
{consultant}

Our team will review your requirements and contact you shortly.

Thank you for choosing Cloud Energy.

Regards,

Cloud Energy Photoelectric Ltd
"""

        EmailService.send(
            subject=subject,
            recipients=[customer.email],
            message=message,
        )

        return True