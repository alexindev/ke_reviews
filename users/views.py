from django.shortcuts import render, reverse, HttpResponseRedirect
from .forms import LoginForm, RegistrationForm
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from users.models import Users


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
                    return HttpResponseRedirect(reverse('users:profile_url'))
        else:
            form = LoginForm()

        context = {
            'title': 'Авторизация пользователей',
            'form': form
        }
        return render(request, 'users/auth.html', context=context)
    return HttpResponseRedirect(reverse('users:profile_url'))

class UserRegustrationView(CreateView):
    template_name = 'users/register.html'
    form_class = RegistrationForm
    model = Users
    success_url = reverse_lazy('users:auth_page_url')


@login_required
def profile_page(request):
    if request.user.is_authenticated:
        context = {
            'title': 'Личный кабинет'
        }
        return render(request, 'users/profile.html', context=context)
    else:
        return HttpResponseRedirect(reverse('users:auth_page_url'))


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('main_app:main_page_url'))
