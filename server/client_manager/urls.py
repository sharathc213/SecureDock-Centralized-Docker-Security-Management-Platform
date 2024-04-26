from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [

    path('sensor/', csrf_exempt(views.CaptureClient.as_view()), name='capture_client_ip'),
    path('enable/', views.EnableSensor.as_view(), name='enable'),
    path('disable/', views.DisableSensor.as_view(), name='disable'),
    path('listclient/', views.ListClient.as_view(), name='listclient'),
    path('deleteclient/', views.DeleteClient.as_view(), name='deleteclient'),
    path('countclient/', views.CountClient.as_view(), name='countclient'),
]
