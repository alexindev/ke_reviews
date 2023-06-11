from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import *


app_name = 'users_cabinet'

urlpatterns = [
    path('', login_required(ProfileUpdateView.as_view()), name='users_profile_url'),
    path('logout/', logout, name='logout_url')

]
