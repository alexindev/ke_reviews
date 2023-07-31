from django.urls import path
from .views import StartPageView, UserLogoutView
from django.contrib.auth.decorators import login_required


app_name = 'start_page'

urlpatterns = [
    path('', StartPageView.as_view(), name='start_page_url'),
    path('logout/', login_required(UserLogoutView.as_view()), name='logout_url'),
]
