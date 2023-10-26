# accounts/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.custom_login, name='login'),
    path('logout/', views.custom_logout, name='logout'), 
    path('profile/', views.user_profile, name='profile'),  
    path('edit-user-profile/', views.edit_user_profile, name='edit_user_profile'),
]
