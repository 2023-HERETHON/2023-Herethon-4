from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('lives/', include('lives.urls')),
    path('accounts/', include('allauth.urls')),
    path('users/', include('users.urls', namespace='users')),
    path('travels/', include('travels.urls')),
    path('dispatch/', include('dispatch.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
