from django.urls import path
from .views import *


app_name = 'main_app'

urlpatterns = [
    path('', MainPageView.as_view(), name='main_page_url'),

]
