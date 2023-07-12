from django.urls import path
from .views import *

urlpatterns = [
  path('', video, name='video')
    # path('admin/', admin.site.urls),
    # path('lives/', include('lives.urls')),
]