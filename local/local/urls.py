from django.contrib import admin
from django.urls import path, include
from lives import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('lives/', include('lives.urls')),
    path('accounts/', include('allauth.urls')),
    path('users/', include('users.urls', namespace='users')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
