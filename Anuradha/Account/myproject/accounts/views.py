# Inside your views.py file
from django.shortcuts import render
#from accounts.models import Account


def create_accounts(request):
    # Create an AWS account
    aws_config = {
        "Access_key": "123",
        "Secret_key": "123432"
    }
    aws_account = Account.objects.create(configuration=aws_config, account_type='aws')
