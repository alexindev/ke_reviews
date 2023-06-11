from django.shortcuts import render
from django.views.generic.base import TemplateView
from common.title import TitleMixin


class MainPageView(TitleMixin, TemplateView):
    template_name = 'main_app/index.html'
    title = 'Главная страница'


def page_not_found(request, exception):
    return render(request, 'page404.html', status=404)
