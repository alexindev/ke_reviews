from django.urls import path
from .views import *

app_name = 'rest'

urlpatterns = [
    path('store_status/', UpdateStoreStatusView.as_view(), name='store_status'),
    path('new_store/', NewStoreView.as_view(), name='new_store'),
    path('review/', ReviewSettingsView.as_view(), name='review'),
    path('avatar/', UserPicView.as_view(), name='avatar'),
    path('delete_store/', DeleteStoreView.as_view(), name='delete_store'),
    path('get_token/', GetNewTokenView.as_view(), name='get_token'),
    path('get_task_status/', GetTaskStatusView.as_view(), name='get_task_status'),
    path('get_reviews/', ReviewsShowView.as_view(), name='get_reviews'),
    path('update_reviews/', ReviewsUpdateView.as_view(), name='update_reviews'),
    path('auth/', UserAuthView.as_view(), name='auth'),
    path('register/', UserRegisterView.as_view(), name='register'),
]