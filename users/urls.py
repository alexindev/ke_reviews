from django.urls import path
from .views import *


app_name = 'users'

urlpatterns = [

    path('register/', RegistrationPageView.as_view(), name='reg_page_url'),
    path('auth/', AuthPageView.as_view(), name='auth_page_url'),

]
