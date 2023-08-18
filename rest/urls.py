from django.urls import path
from .views import *

app_name = 'rest'

urlpatterns = [
    path('store_status/', UpdateStoreStatusView.as_view()),
    path('new_store/', NewStoreView.as_view()),
    path('review/', ReviewSettingsView.as_view()),
    path('avatar/', UserPicView.as_view()),
    path('delete_store/', DeleteStoreView.as_view()),
    path('get_token/', GetNewTokenView.as_view()),
    path('get_task_status/', GetTaskStatusView.as_view()),
    path('get_reviews/', ReviewsShowView.as_view()),
    path('update_reviews/', ReviewsUpdateView.as_view()),
    path('auth/', UserAuthView.as_view(), name='auth'),
    path('register/', UserRegisterView.as_view(), name='register'),
]