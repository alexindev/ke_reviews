from django.shortcuts import render, reverse, HttpResponseRedirect
from .forms import LoginForm, RegisterForm
from django.contrib import auth


def auth_page(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('main_app:main_page_url'))
    else:
        form = LoginForm()

    context = {
        'title': 'Авторизация пользователей',
        'form': form
    }
    return render(request, 'users/auth.html', context=context)


def reg_page(request):
    if request.method == 'POST':
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('users:auth_page_url'))
    else:
        form = RegisterForm()

    context = {
        'title': 'Регистрация пользователей',
        'form': form
    }
    return render(request, 'users/register.html', context=context)
