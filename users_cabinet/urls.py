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
    path('settings/api/v1/store_status/', UpdateStoreStatusView.as_view()),
    path('settings/api/v1/new_store/', NewStoreView.as_view()),
    path('settings/api/v1/review/', ReviewDataView.as_view()),
    path('settings/api/v1/avatar/', UserPicView.as_view()),
    path('settings/api/v1/delete_store/', DeleteStoreView.as_view()),
    path('settings/api/v1/get_token/', GetNewTokenView.as_view()),
    path('settings/api/v1/get_token_status/', GetTokenStatusView.as_view()),
    path('reviews/api/v1/get_reviews/', ReviewsShowView.as_view()),
    path('reviews/api/v1/update_reviews/', ReviewsUpdateView.as_view()),
]
