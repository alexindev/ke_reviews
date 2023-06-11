from django.contrib import auth
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, reverse, HttpResponseRedirect
from django.views.generic.edit import CreateView

from django.urls import reverse_lazy

from users.models import Users
from common.title import TitleMixin
from .forms import LoginForm, RegistrationForm


class UserRegustrationView(TitleMixin, SuccessMessageMixin, CreateView):
    template_name = 'users/register.html'
    form_class = RegistrationForm
    model = Users
    success_url = reverse_lazy('users:auth_page_url')
    success_message = 'Регистрация выполнена успешно'
    title = 'Регистрация пользователей'


def auth_page(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = LoginForm(data=request.POST)
            if form.is_valid():
                username = request.POST['username']
                password = request.POST['password']
                user = auth.authenticate(username=username, password=password)
                if user:
                    auth.login(request, user)
                    return HttpResponseRedirect(reverse('users_cabinet:users_profile_url'))
        else:
            form = LoginForm()

        context = {
            'title': 'Авторизация пользователей',
            'form': form
        }
        return render(request, 'users/auth.html', context=context)
    return HttpResponseRedirect(reverse('users_cabinet:users_profile_url'))

