from django.db import models
import json

class ConfigurationData(models.Model):
    ACCOUNT_TYPES = [
        ('AWS', 'AWS'),
        ('Azure', 'Azure'),
        
    ]

    account_name = models.CharField(max_length=255, unique=True)
    account_type = models.CharField(max_length=50, choices=ACCOUNT_TYPES)
    configuration = models.JSONField()

    def save_configuration(self, data):
       
        self.configuration = json.dumps(data)#This is dumps methord will be used to convert python objectes into jason string
    
    def get_configuration(self):
        
        return json.loads(self.configuration)# this will do the vice-versa fo the above code 

    def __str__(self):
        return f'{self.account_name} - {self.account_type}'

