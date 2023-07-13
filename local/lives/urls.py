from django.urls import path
from .views import *


app_name = "lives"

urlpatterns = [
  path('cam/', live_stream, name='live_stream'),
  path('create/', live_create, name='live_create'),
  path('', live_list, name='live_list'),
  path('detail/<int:pk>', live_detail, name='live_detail'),
]