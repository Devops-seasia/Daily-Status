from django.db import models

class Account(models.Model):
    id = models.AutoField(primary_key=True)
    configuration = models.JSONField()
    account_type = models.CharField(max_length=10)
