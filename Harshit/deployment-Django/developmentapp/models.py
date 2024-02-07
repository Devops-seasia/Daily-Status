from django.db import models
import json

class ConfigurationData(models.Model):
    ACCOUNT_TYPES = [
        ('AWS', 'AWS'),
        ('Azure', 'Azure'),
        # Add more account types as needed
    ]

    account_name = models.CharField(max_length=255, unique=True)
    account_type = models.CharField(max_length=50, choices=ACCOUNT_TYPES)
    configuration = models.JSONField()

    def save_configuration(self, data):
        # Save JSON data to the model
        self.configuration = json.dumps(data)
    
    def get_configuration(self):
        # Retrieve JSON data from the model
        return json.loads(self.configuration)

    def __str__(self):
        return f'{self.account_name} - {self.account_type}'

