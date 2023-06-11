from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import *


app_name = 'users_cabinet'

urlpatterns = [
    path('dashboard/', login_required(ProfileDetailView.as_view()), name='users_profile_url'),
    path('settings/', login_required(SettingsTemplateView.as_view()), name='profile_settings_url'),
    path('parser/', login_required(ParserTemplateView.as_view()), name='parser_url'),
    path('reviews/', login_required(ReviewsTemplateView.as_view()), name='reviews_url'),
    path('logout/', logout, name='logout_url'),


]
