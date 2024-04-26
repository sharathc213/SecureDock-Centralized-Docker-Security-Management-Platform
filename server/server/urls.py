
from django.contrib import admin
from django.urls import path , include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('authentication.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('download/', include('downloade.urls')),
    path('client/', include('client_manager.urls')),

]
