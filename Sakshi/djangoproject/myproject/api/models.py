# models.py
from django.db import models

class Account(models.Model):
    id = models.AutoField(primary_key=True)
    
    account_type = models.CharField(max_length=255)
    configuration = models.JSONField()
    def __str__(self):
        return self.details
     

