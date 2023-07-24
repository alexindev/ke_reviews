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
    path('get_token/', GetTokenView.as_view(), name='get_token_url'),
    path('settings/<int:store_id>/', DeleteStoreView.as_view(), name='delete_store_url'),
    path('settings/api/v1/store_status/<int:store_id>/', UpdateStoreStatusView.as_view(), name='update_store_status_url'),
    path('settings/api/v1/new_store/', NewStoreView.as_view(), name='new_store_url'),
    path('settings/api/v1/review/', ReviewDataView.as_view(), name='review_data_url'),
    path('settings/api/v1/avatar/', UserPicView.as_view(), name='user_pic_url'),

]
