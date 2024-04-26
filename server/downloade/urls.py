from django.urls import path
from . import views

urlpatterns = [
    path('setup/', views.SetupDownloadView.as_view(), name='setup-download'),
    path('client/', views.ClientDownloadView.as_view(), name='client-download'),
]
