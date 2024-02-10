
from django.urls import path
from .views import ConfigurationDataCreateAPIView
from .views import get_all_data

urlpatterns = [
    path('api/', ConfigurationDataCreateAPIView.as_view(), name='create-configuration-data'),
    path('all-data/',get_all_data, name='all_data'),
   
]