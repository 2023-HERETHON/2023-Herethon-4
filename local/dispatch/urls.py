from django.urls import path
from . import views
from .views import *

app_name = "dispatch"

urlpatterns = [
    # path('', views.whole_list, name='whole_list'),
    path('', views.whole_list, name='all_list'),
    path('near_list', views.near_list, name='near_list'),
    path('my_list', views.my_list, name='my_list'),
    path('post/', views.dispatch_post, name='dispatch_post'),
    path('<int:pk>/', views.dispatch_detail, name="dispatch_detail"),

    # path('<int:pk>/comment/', views.comments_create, name='comments_create'),

]