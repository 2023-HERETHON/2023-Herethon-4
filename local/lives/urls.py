from django.urls import path
from .views import *


app_name = "lives"

urlpatterns = [
  path('cam/', live_stream, name='live_stream'),
  path('create/', live_create, name='live_create'),
  path('', live_list, name='live_list'),
  path('recent/', live_recent, name='live_recent'),
  path('soon/', live_soon, name='live_soon'),
  path("likes/<int:pk>/", live_likes, name='live_likes'),
  path('detail/<int:pk>', live_detail, name='live_detail'),
]