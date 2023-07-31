from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
from common.title import TitleMixin


class StartPageView(TitleMixin, TemplateView):
    template_name = 'start_page/index.html'
    title = 'Главная страница'


class UserLogoutView(LogoutView):
    """Разлогиниться"""
    next_page = reverse_lazy('start_page:start_page_url')


def page_not_found(request, exception):
    return render(request, 'page404.html', status=404)
