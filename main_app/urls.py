from django.urls import path
from .views import *


app_name = 'main_app'

urlpatterns = [
    path('', MainPage.as_view(), name='main_page_url'),
    path('register/', reg_page, name='reg_page_url'),
    path('auth/', auth_page, name='auth_page_url'),
]
