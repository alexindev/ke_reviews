from django.shortcuts import render, reverse, HttpResponseRedirect
from .forms import LoginForm, RegistrationForm
from django.contrib import auth
from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView
from django.urls import reverse_lazy
from users.models import Users


class UserRegustrationView(CreateView):
    template_name = 'users/register.html'
    form_class = RegistrationForm
    model = Users
    success_url = reverse_lazy('users:auth_page_url')

    def get_context_data(self, **kwargs):
        context = super(UserRegustrationView, self).get_context_data()
        context['title'] = 'Регистрация пользователей'
        return context


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
                    return HttpResponseRedirect(reverse('users:profile_url', args=(request.user.pk,)))
        else:
            form = LoginForm()

        context = {
            'title': 'Авторизация пользователей',
            'form': form
        }
        return render(request, 'users/auth.html', context=context)
    return HttpResponseRedirect(reverse('users:profile_url', args=(request.user.pk,)))


class ProfileUpdateView(TemplateView):
    template_name = 'users/profile.html'

    def get_context_data(self, **kwargs):
        context = super(ProfileUpdateView, self).get_context_data()
        context['title'] = 'Личный кабинет'
        return context


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('main_app:main_page_url'))
