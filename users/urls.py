from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required


app_name = 'users'

urlpatterns = [

    path('register/', UserRegustrationView.as_view(), name='reg_page_url'),
    path('auth/', auth_page, name='auth_page_url'),
    path('profile/<int:pk>/', login_required(ProfileUpdateView.as_view()), name='profile_url'),
    path('logout/', logout, name='logout_url')
]
