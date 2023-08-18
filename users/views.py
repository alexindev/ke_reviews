from django.contrib.auth.views import LoginView
from django.views.generic import TemplateView

from common.title import TitleMixin


class RegistrationPageView(TitleMixin, TemplateView):
    """Регистрация пользователей"""
    template_name = 'users/register.html'
    title = 'Регистрация пользователей'


class AuthPageView(TitleMixin, LoginView):
    """Авторизация пользователей"""
    template_name = 'users/auth.html'
    title = 'Авторизация пользователей'

