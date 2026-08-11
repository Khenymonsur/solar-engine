from crm.models import SalesProfile


class ReferralMiddleware:
    """
    Capture a salesperson referral code from the URL
    and store it in the user's session.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        referral = request.GET.get("ref")

        if referral:

            # Don't query the database again if the same referral
            # is already stored in the session.
            if request.session.get("sales_ref") != referral:

                profile = SalesProfile.objects.filter(
                    referral_code=referral,
                    active=True,
                ).first()

                if profile:

                    request.session["sales_ref"] = profile.referral_code
                    request.session["sales_profile_id"] = profile.pk
                    request.session.modified = True

        return self.get_response(request)