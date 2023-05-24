from django.shortcuts import render, HttpResponse
from django.views import View


class MainPage(View):
    template_name = 'ke_app/index.html'

    def get(self, request):
        return render(request, self.template_name)

def page_var(request, variable):
    return HttpResponse(f'<h1>Страница с переменной {variable}</h1>')

def page_varvar(request):
    if request.GET:
        print(request.GET)
    return HttpResponse('<h1>Страница без переменной</h1>')

def reg_page(request):
    return render(request, 'ke_app/register.html')


def page_not_found(request, exception):
    return render(request, 'ke_app/page404.html', status=404)
