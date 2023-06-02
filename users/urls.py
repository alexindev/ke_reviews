from django.urls import path
from .views import *


app_name = 'users'

urlpatterns = [

    path('register/', reg_page, name='reg_page_url'),
    path('auth/', auth_page, name='auth_page_url'),
    path('cabinet/', cabinet_page, name='caninet_url')
]
