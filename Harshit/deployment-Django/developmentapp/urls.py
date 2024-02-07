
from django.urls import path
from .views import ConfigurationDataCreateAPIView

urlpatterns = [
    path('api/', ConfigurationDataCreateAPIView.as_view(), name='create-configuration-data'),
   
]