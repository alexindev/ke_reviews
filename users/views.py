from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

from users.models import User
from common.title import TitleMixin
from .forms import LoginForm, RegistrationForm


class UserRegustrationView(TitleMixin, SuccessMessageMixin, CreateView):
    template_name = 'users/register.html'
    form_class = RegistrationForm
    model = User
    success_url = reverse_lazy('users:auth_page_url')
    success_message = 'Регистрация выполнена успешно'
    title = 'Регистрация пользователей'


class UserAuthView(TitleMixin, LoginView):
    template_name = 'users/auth.html'
    success_url = reverse_lazy('users_cabinet:users_profile_url')
    form_class = LoginForm
    redirect_authenticated_user = True
    title = 'Авторизация пользователей'

