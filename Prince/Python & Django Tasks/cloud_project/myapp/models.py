from django.db import models

# Create your models here.
# Register your models here.
# models.py
from django.db import models

class ConfigurationData(models.Model):
    account_name = models.CharField(max_length=255)
    account_type = models.CharField(max_length=255)
    configuration = models.JSONField()

    def __str__(self):
        return self.config_name