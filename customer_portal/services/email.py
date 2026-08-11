from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


class EmailService:
    """
    Central email service.

    Supports:
    - Plain text emails
    - HTML template emails
    """

    @staticmethod
    def send(
        *,
        subject,
        recipients,
        message=None,
        template=None,
        context=None,
        fail_silently=False,
    ):

        if not recipients:
            return False

        # ----------------------------
        # Plain Text Email
        # ----------------------------

        if template is None:

            email = EmailMultiAlternatives(
                subject=subject,
                body=message or "",
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=recipients,
            )

            email.send(
                fail_silently=fail_silently,
            )

            return True

        # ----------------------------
        # HTML Email
        # ----------------------------

        context = context or {}

        html_message = render_to_string(
            template,
            context,
        )

        try:
            text_message = render_to_string(
                "emails/plain.txt",
                context,
            )
        except Exception:
            text_message = ""

        email = EmailMultiAlternatives(
            subject=subject,
            body=text_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=recipients,
        )

        email.attach_alternative(
            html_message,
            "text/html",
        )

        email.send(
            fail_silently=fail_silently,
        )

        return True