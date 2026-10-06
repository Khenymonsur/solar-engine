import logging

from django.conf import settings
from django.urls import reverse
from django.utils import timezone

from .email import EmailService


logger = logging.getLogger(__name__)


class AssessmentNotificationService:
    """
    Handles notifications related to customer assessments.
    """

    # =========================================================
    # SALES CONSULTANT NOTIFICATION
    # =========================================================

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
                kwargs={
                    "pk": assessment.pk,
                },
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
Reference: {assessment.reference}
Project: {assessment.project_name}
Connected Load: {assessment.connected_load:,.0f} W
Status: {assessment.status}

View Assessment
---------------
{assessment_url}

Please log into the Staff Portal and follow up with this customer.

Regards,

Cloud Energy Photoelectric Ltd
"""

        return EmailService.send(
            subject=subject,
            recipients=[sales_user.email],
            message=message,
        )


    # =========================================================
    # CUSTOMER CONFIRMATION
    # =========================================================

    @staticmethod
    def send_customer_confirmation(request, assessment):
        """
        Send branded assessment confirmation email
        to the customer.
        """

        customer = assessment.customer

        # -----------------------------------------
        # No email address
        # -----------------------------------------

        if not customer.email:
            logger.warning(
                "Customer confirmation skipped. "
                "Customer %s has no email address.",
                customer.pk,
            )

            return False

        # -----------------------------------------
        # Prevent duplicate confirmation
        # -----------------------------------------

        if assessment.customer_confirmation_sent:

            logger.info(
                "Customer confirmation already sent "
                "for assessment %s.",
                assessment.reference,
            )

            return True

        # -----------------------------------------
        # Consultant
        # -----------------------------------------

        consultant_name = "Cloud Energy Sales Team"

        if assessment.assigned_sales:

            sales_user = assessment.assigned_sales.user

            consultant_name = (
                sales_user.get_full_name()
                or sales_user.username
            )

        # -----------------------------------------
        # Customer assessment URL
        # -----------------------------------------

        assessment_url = request.build_absolute_uri(
            reverse(
                "customer_portal:assessment-detail",
                kwargs={
                    "pk": assessment.pk,
                },
            )
        )

        # -----------------------------------------
        # Assessment date
        # -----------------------------------------

        assessment_date = timezone.localtime(
            assessment.created_at
        ).strftime("%d %b %Y")

        # -----------------------------------------
        # Email context
        # -----------------------------------------

        context = {

            "customer_name": customer.full_name,

            "assessment_reference": assessment.reference,

            "assessment_date": assessment_date,

            "connected_load": (
                f"{assessment.connected_load:,.0f} W"
            ),

            "status": assessment.status,

            "consultant_name": consultant_name,

            "property_address": customer.address,

            "assessment_url": assessment_url,

            "logo_url": settings.EMAIL_LOGO_URL,
        }

        # -----------------------------------------
        # Subject
        # -----------------------------------------

        subject = (
            "Solar Assessment Received - "
            f"{assessment.reference}"
        )

        # -----------------------------------------
        # Send email
        # -----------------------------------------

        sent = EmailService.send(

            subject=subject,

            recipients=[
                customer.email,
            ],

            template=(
                "emails/assessment_received.html"
            ),

            text_template=(
                "emails/assessment_received.txt"
            ),

            context=context,

            fail_silently=False,
        )

        # -----------------------------------------
        # Mark confirmation as sent
        # -----------------------------------------

        if sent:

            assessment.customer_confirmation_sent = True

            assessment.customer_confirmation_sent_at = (
                timezone.now()
            )

            assessment.save(
                update_fields=[
                    "customer_confirmation_sent",
                    "customer_confirmation_sent_at",
                ]
            )

            logger.info(
                "Customer confirmation sent: %s",
                assessment.reference,
            )

        return sent