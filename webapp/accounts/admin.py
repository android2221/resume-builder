from django.contrib import admin
from accounts.models import Account

# Register your models here.

class AccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'profile_url')
    search_fields = ['user__username', 'profile_url']

admin.site.register(Account, AccountAdmin)
