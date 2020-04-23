from django.conf import settings

def get_production_setting(request):
    return { 'is_production': settings.IS_PRODUCTION }