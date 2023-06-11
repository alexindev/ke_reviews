from common.title import TitleMixin
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.contrib import auth
from django.shortcuts import reverse, HttpResponseRedirect
from users.models import Users


class ProfileDetailView(TitleMixin, ListView):
    template_name = 'users_cabinet/profile.html'
    model = Users
    title = 'Главное меню'


class SettingsTemplateView(TitleMixin, ListView):
    template_name = 'users_cabinet/settings.html'
    model = Users
    title = 'Настройки'


class ParserTemplateView(TitleMixin, ListView):
    template_name = 'users_cabinet/parser.html'
    model = Users
    title = 'Парсер'


class ReviewsTemplateView(TitleMixin, ListView):
    template_name = 'users_cabinet/reviews.html'
    model = Users
    title = 'Отзывы'


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('main_app:main_page_url'))
