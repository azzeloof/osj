from osj import settings

def google_analytics_key(request):
    return {'google_analytics_key': settings.GOOGLE_ANALYTICS_KEY}

def kofi_creds(request):
    return {
        'kofi_username': settings.KOFI_USERNAME,
        'kofi_key': settings.KOFI_KEY
        }
