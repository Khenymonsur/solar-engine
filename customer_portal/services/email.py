from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


class EmailService:
    """
    Central email service for the Cloud Energy platform.

    Supports:
    - Plain text emails
    - HTML emails
    - Plain-text fallback templates
    - Reply-To addresses
    """

    @staticmethod
    def send(
        *,
        subject,
        recipients,
        message=None,
        template=None,
        text_template=None,
        context=None,
        reply_to=None,
        fail_silently=False,
    ):
        """
        Send an email.

        Parameters
        ----------
        subject:
            Email subject.

        recipients:
            List of recipient email addresses.

        message:
            Optional plain-text message.

        template:
            Optional HTML template.

        text_template:
            Optional plain-text template.

        context:
            Template context dictionary.

        reply_to:
            Optional list of Reply-To email addresses.

        fail_silently:
            Whether Django should suppress email errors.
        """

        if not recipients:
            return False

        context = context or {}

        # -----------------------------------------
        # Plain-text body
        # -----------------------------------------

        if text_template:

            text_message = render_to_string(
                text_template,
                context,
            )

        else:

            text_message = message or ""

        # -----------------------------------------
        # Create email
        # -----------------------------------------

        email = EmailMultiAlternatives(
            subject=subject,
            body=text_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=recipients,
            reply_to=reply_to or None,
        )

        # -----------------------------------------
        # HTML alternative
        # -----------------------------------------

        if template:

            html_message = render_to_string(
                template,
                context,
            )

            email.attach_alternative(
                html_message,
                "text/html",
            )

        # -----------------------------------------
        # Send
        # -----------------------------------------

        sent_count = email.send(
            fail_silently=fail_silently,
        )

        return sent_count > 0