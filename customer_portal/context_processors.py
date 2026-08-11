from audits.models import Assessment


def customer_project(request):
    """
    Make the customer's latest assessment available
    throughout the customer portal.
    """

    latest_assessment = None

    if request.user.is_authenticated:

        latest_assessment = (
            Assessment.objects
            .filter(customer__user=request.user)
            .order_by("-created_at")
            .first()
        )

    return {
        "latest_assessment": latest_assessment
    }