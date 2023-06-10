from django.shortcuts import render
from django.views.generic.base import TemplateView


class MainPageView(TemplateView):
    template_name = 'main_app/index.html'


def page_not_found(request, exception):
    return render(request, 'page404.html', status=404)
