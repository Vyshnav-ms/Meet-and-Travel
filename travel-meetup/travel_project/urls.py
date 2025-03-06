from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from trips.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('users/', include('users.urls')),
    path('trips/', include('trips.urls')),
    path('messages/', include('messages_app.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)