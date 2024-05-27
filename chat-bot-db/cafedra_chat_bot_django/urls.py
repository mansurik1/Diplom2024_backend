from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('calendar_api/v1/', include('calendar_module.api_v1.urls')),
]
