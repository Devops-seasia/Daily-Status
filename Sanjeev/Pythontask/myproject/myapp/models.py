from django.db import models

# Create your models here.

class Accounts(models.Model):
    acc_id = models.CharField(max_length=200)
    account_type = models.CharField(max_length=10)
    configurations = models.JSONField()


    def __str__(self):
        return str(self.acc_id)
    
