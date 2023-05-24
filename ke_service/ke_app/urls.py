from django.urls import path
from .views import *


urlpatterns = [
    path('', MainPage.as_view(), name='main_page_url'),
    path('register/', reg_page, name='reg_page_url'),
    path('var/', page_varvar),
    path('var/<str:variable>/', page_var, name='variable'),
]