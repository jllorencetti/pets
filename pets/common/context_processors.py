from django.conf import settings


def analytics(request):
    return {"GOOGLE_API_KEY": settings.GOOGLE_API_KEY, "HOTJAR_TRACKING_KEY": settings.HOTJAR_TRACKING_KEY}
