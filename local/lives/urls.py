from django.urls import path
from .views import *


app_name = "lives"

urlpatterns = [
  path('create/', live_stream, name='live_stream'),
  path('', live_list, name='live_list'),
]