from django.shortcuts import render
from django.views import View


class MainPage(View):
    template_name = 'main_app/index.html'

    def get(self, request):
        return render(request, self.template_name)


def auth_page(request):
    context = {'title': 'Авторизация пользователей'}
    return render(request, 'main_app/auth.html', context=context)


def reg_page(request):
    context = {'title': 'Регистрация пользователей'}
    return render(request, 'main_app/register.html', context=context)


def page_not_found(request, exception):
    return render(request, 'page404.html', status=404)
