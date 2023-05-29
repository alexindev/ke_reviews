from django.shortcuts import render
from django.views import View


class MainPage(View):
    template_name = 'main_app/index.html'

    def get(self, request):
        return render(request, self.template_name)


def auth_page(request):
    return render(request, 'main_app/auth.html')


def reg_page(request):
    return render(request, 'main_app/register.html')


def page_not_found(request, exception):
    return render(request, 'page404.html', status=404)
