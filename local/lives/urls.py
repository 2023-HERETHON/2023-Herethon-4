from django.urls import path
from .views import *


app_name = "lives"

urlpatterns = [
  path('', live_stream, name='live_stream'),
]