from django.urls import path
from .views import StartPageView


app_name = 'start_page'

urlpatterns = [
    path('', StartPageView.as_view(), name='main_page_url'),

]
