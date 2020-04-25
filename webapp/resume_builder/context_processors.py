from django.conf import settings

def get_production_setting(request):
    return { 
        'IS_PRODUCTION': settings.IS_PRODUCTION,
        'ACTIVATE_GOOGLE_ANALYTICS': settings.ACTIVATE_GOOGLE_ANALYTICS
     }