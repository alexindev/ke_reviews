from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import *


app_name = 'users_cabinet'

urlpatterns = [
    path('dashboard/', login_required(ProfileView.as_view()), name='users_profile_url'),
    path('settings/', login_required(SettingsView.as_view()), name='profile_settings_url'),
    path('parser/', login_required(ParserView.as_view()), name='parser_url'),
    path('reviews/', login_required(ReviewsView.as_view()), name='reviews_url'),
    path('logout/', UserLogoutView.as_view(), name='logout_url'),
    path('delete_profile/', DeleteProfileView.as_view(), name='delete_profile_url'),
    path('settings/<int:store_id>', delete_store, name='delete_store_url'),
    path('get_token/', GetTokenView.as_view(), name='get_token_url'),
]
