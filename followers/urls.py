# followers/urls.py
from django.urls import path
from .views import follow_user

urlpatterns = [
    path('<str:username>/follow/', follow_user, name='follow_user'),
]