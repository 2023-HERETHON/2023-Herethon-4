from django.urls import path
from .views import *

app_name = "travels"

urlpatterns = [
  path('', travel_list, name='travel_list'),
  path('<int:pk>/', travel_detail, name='travel_detail'),
  path("likes/<int:pk>/", travel_likes, name='travel_likes'),
  path('create/', travel_create, name='travel_creaet'),
  # path('delete/<int:pk>/', travel_delete, name='travel_delete'),
]