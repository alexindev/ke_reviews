from django.shortcuts import render, reverse, HttpResponseRedirect, redirect
from .forms import LoginForm, RegisterForm
from django.contrib import auth


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
                    return HttpResponseRedirect(reverse('users:caninet_url'))
        else:
            form = LoginForm()

        context = {
            'title': 'Авторизация пользователей',
            'form': form
        }
        return render(request, 'users/auth.html', context=context)
    else:
        return redirect(reverse('users:caninet_url'))

def reg_page(request):
    if not request.user.is_authenticated:
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
    else:
        return redirect(reverse('users:caninet_url'))

def cabinet_page(request):
    context = {
        'title': 'Личный кабинет'
    }
    return render(request, 'users/cabinet.html', context=context)
