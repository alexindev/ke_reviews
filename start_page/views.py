from django.shortcuts import render
from django.views.generic.base import TemplateView
from common.title import TitleMixin


class StartPageView(TitleMixin, TemplateView):
    template_name = 'start_page/index.html'
    title = 'Главная страница'


def page_not_found(request, exception):
    return render(request, 'page404.html', status=404)
