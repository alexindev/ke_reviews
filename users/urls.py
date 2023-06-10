from django.urls import path
from .views import *


app_name = 'users'

urlpatterns = [

    path('register/', UserRegustrationView.as_view(), name='reg_page_url'),
    path('auth/', auth_page, name='auth_page_url'),
    path('profile/', profile_page, name='profile_url'),
    path('logout/', logout, name='logout_url')
]
