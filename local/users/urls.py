from django.contrib import admin
from django.urls import path, include
from users import views

app_name = "users"

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('signup/more-info', views.input_info, name='more_info'),
    path('login/', views.login, name='login'),
    path('id-login', views.id_login, name='id_login' ),
    path('logout/', views.logout, name='logout'),
    path('user/', views.user_view, name='user_list'),
    path('user/follow/<int:id>/<int:pk>/', views.user_follow, name='user_follow'),
    path('mypage/', views.mypage, name='mypage'),
]