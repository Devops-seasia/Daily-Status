from django.contrib import admin
from django.urls import path, include
from myapp.views import AccountView

urlpatterns = [
    path('postdata/', AccountView.as_view(), name='data')
    
]