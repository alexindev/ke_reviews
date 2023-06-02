from django.urls import path
from .views import *


app_name = 'main_app'

urlpatterns = [
    path('', main_page, name='main_page_url'),

]
