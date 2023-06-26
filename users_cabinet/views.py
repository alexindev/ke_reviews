from django.views import View
from django.views.generic.list import ListView
from django.views.generic.edit import FormView
from django.contrib.auth.views import LogoutView
from django.contrib.auth import logout
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from datetime import datetime, timedelta
from django.contrib import messages

from users.models import Users
from .models import UserStores

from common.title import TitleMixin
from .forms import UserPicForm, UserDataForm, StoreForm

from .utils.stores import get_store
from .tasks import new_token


class ProfileView(TitleMixin, ListView):
    template_name = 'users_cabinet/profile.html'
    model = Users
    title = 'Главное меню'


class SettingsView(TitleMixin, SuccessMessageMixin, FormView):
    template_name = 'users_cabinet/settings.html'
    title = 'Настройки'
    form_class = StoreForm
    success_message = 'Данные обновлены'
    success_url = reverse_lazy('users_cabinet:profile_settings_url')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['avatar_form'] = UserPicForm(instance=self.request.user)
        context['user_data_form'] = UserDataForm(instance=self.request.user)
        context['store_form'] = StoreForm()
        store_urls = UserStores.objects.filter(user_id=self.request.user.pk).values('id', 'store__store_url')
        context['store_urls'] = store_urls
        return context

    def form_valid(self, form):
        if 'avatar_btn' in self.request.POST:
            avatar_form = UserPicForm(self.request.POST, self.request.FILES, instance=self.request.user)
            if avatar_form.is_valid():
                avatar_form.save()

        elif 'user_data_btn' in self.request.POST:
            user_data_form = UserDataForm(self.request.POST, instance=self.request.user)
            if user_data_form.is_valid():
                user_data_form.save()

        elif 'store_btn' in self.request.POST:
            store_form = StoreForm(self.request.POST)
            if store_form.is_valid():
                store_url = store_form.cleaned_data['store_url']
                if not UserStores.objects.filter(user=self.request.user, store__store_url=store_url).exists():
                    if get_store(store_url):
                        store = store_form.save()
                        UserStores.objects.create(store=store, user=self.request.user)
                    else:
                        form.add_error('store_url', 'Некорректная ссылка или магазина не существует')
                        return super().form_invalid(form)
                else:
                    form.add_error('store_url', 'Магазина уже добавлен')
                    return super().form_invalid(form)
        return super().form_valid(form)


class ParserView(TitleMixin, ListView):
    template_name = 'users_cabinet/parser.html'
    model = UserStores
    title = 'Парсер'

    def get_queryset(self):
        period = self.request.GET.get('period-select')
        store = self.request.GET.get('store-select')
        queryset = UserStores.objects.filter(user=self.request.user, store__store_url=store)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['store_urls'] = UserStores.objects.filter(user=self.request.user).values('store__store_url')
        return context


class ReviewsView(TitleMixin, ListView):
    template_name = 'users_cabinet/reviews.html'
    model = Users
    title = 'Отзывы'


class GetTokenView(View):
    def post(self, request):
        user = request.user
        login = user.login_ke
        password = user.pass_ke
        new_token.delay(login, password)
        messages.success(request, 'Получаем токен...')
        return redirect('users_cabinet:profile_settings_url')


class DeleteProfileView(View):
    def post(self, request, *args, **kwargs):
        self.request.user.delete()
        logout(request)
        return redirect(reverse_lazy('users:auth_page_url'))


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('main_app:main_page_url')


def delete_store(request, store_id):
    UserStores.objects.filter(id=store_id).delete()
    return redirect(reverse_lazy('users_cabinet:profile_settings_url'))
