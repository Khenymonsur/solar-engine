from django.conf import settings

def google_maps(request):
    return {
        "GOOGLE_MAPS_API_KEY": settings.GOOGLE_MAPS_API_KEY
    }


def session_timeout(request):
    return {
        "SESSION_TIMEOUT": settings.SESSION_TIMEOUT,
        "SESSION_WARNING_TIME": settings.SESSION_WARNING_TIME,
    }