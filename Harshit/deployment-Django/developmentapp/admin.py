from django.contrib import admin
from .models import ConfigurationData

@admin.register(ConfigurationData)#model with the Django admin interface. This allows you to manage instances of this model through the admin interface.
class ConfigurationDataAdmin(admin.ModelAdmin):
    list_display = ('account_name', 'account_type',)#list_display: This attribute specifies which fields of the model should be displayed in the list view of the admin interface
    search_fields = ('account_name', 'account_type',)#his attribute specifies which fields of the model should be searchable in the admin interface