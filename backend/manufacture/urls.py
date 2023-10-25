from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('api/docs/', include('api.docs')),
    path('__debug__/', include('debug_toolbar.urls')),
]
