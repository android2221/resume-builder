from django.conf import settings


def get_production_setting(request):
    return { 
        'IS_PRODUCTION': settings.IS_PRODUCTION,
        'ACTIVATE_GOOGLE_ANALYTICS': settings.ACTIVATE_GOOGLE_ANALYTICS
     }

def add_url_setting(request):
    return {
        'FEEDBACK_FORM_URL': settings.FEEDBACK_FORM_URL,
        'SUPPORT_FORM_URL': settings.SUPPORT_FORM_URL
    }
