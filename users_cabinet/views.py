from common.title import TitleMixin
from django.views.generic.base import TemplateView
from django.contrib import auth
from django.shortcuts import reverse, HttpResponseRedirect


class ProfileUpdateView(TitleMixin, TemplateView):
    template_name = 'users_cabinet/index.html'
    title = 'Личный кабинет'

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('main_app:main_page_url'))
