# accounts/urls.py
from django.urls import path
from . import views

urlpatterns = [
    
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
     path('users/',views.user_list,name='user_list'),
    path('password-change/', views.custom_password_change, name='custom_password_change'),
     
    path('<str:username>/', views.profile, name='profile'),
   
    
]