from django.contrib import admin
from .models import ConfigurationData

@admin.register(ConfigurationData)
class ConfigurationDataAdmin(admin.ModelAdmin):
    list_display = ('account_name', 'account_type',)
    search_fields = ('account_name', 'account_type',)