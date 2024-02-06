# urls.py
from django.urls import path
from .views import CreateConfigAPIView

urlpatterns = [
    path('configuration-data-create/', CreateConfigAPIView.as_view(), name='create-config'),
]
