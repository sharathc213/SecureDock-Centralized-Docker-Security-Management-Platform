from . import views
from django.urls import path,include



urlpatterns = [
   
    path('',views.Index.as_view(),name='index'),
    path('check-button-status/',views.CheckButtonStatus.as_view(),name='CheckButtonStatus'),
    path('scan-client/',views.ScanView.as_view(),name='scan_view'),

    
]