from common.title import TitleMixin
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from users.models import Users
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy


class ProfileView(TitleMixin, ListView):
    template_name = 'users_cabinet/profile.html'
    model = Users
    title = 'Главное меню'


class SettingsView(TitleMixin, ListView):
    template_name = 'users_cabinet/settings.html'
    model = Users
    title = 'Настройки'


class ParserView(TitleMixin, ListView):
    template_name = 'users_cabinet/parser.html'
    model = Users
    title = 'Парсер'


class ReviewsView(TitleMixin, ListView):
    template_name = 'users_cabinet/reviews.html'
    model = Users
    title = 'Отзывы'


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('main_app:main_page_url')

