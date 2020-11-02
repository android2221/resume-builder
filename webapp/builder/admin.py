from django.contrib import admin
from builder.models import Resume

# Register your models here.

class ResumeAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ['user__username',]


admin.site.register(Resume, ResumeAdmin)
