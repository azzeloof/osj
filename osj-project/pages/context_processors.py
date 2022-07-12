from osj import settings

def google_analytics_key(request):
    return {'google_analytics_key': settings.GOOGLE_ANALYTICS_KEY}