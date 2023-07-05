from django.views.generic.list import ListView
from django.views.generic.edit import FormView
from django.views.generic.base import RedirectView
from django.contrib.auth.views import LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import logout
from django.contrib import messages
from django.urls import reverse_lazy

from datetime import date, timedelta

from .models import *
from .forms import UserPicForm, UserDataForm, StoreForm

from common.title import TitleMixin
from users_cabinet.tasks import review_manager, parser_manager, new_token
from .utils.stores import get_store


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

        store_urls = Stores.objects.filter(userstores__user=self.request.user).values('id', 'store_url', 'action')
        context['stores'] = store_urls

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['period'] = range(1, 8)
        store_url = self.request.GET.get('store-select')
        period = int(self.request.GET.get('period-select', 1))

        start_date = date.today() - timedelta(days=period)

        context['data'] = UserStores.objects.filter(store__store_url=store_url, datetime__gte=start_date)
        return context


class ReviewsView(TitleMixin, ListView):
    template_name = 'users_cabinet/reviews.html'
    title = 'Отзывы'
    model = Reviews
    ordering = '-date_create'
    paginate_by = 20

    def post(self, request, *args, **kwargs):
        user = Users.objects.get(id=request.user.pk)
        token = user.token
        user_pk = user.pk
        review_manager.delay(token, user_pk)
        return self.get(request, *args, **kwargs)


class DeleteProfileView(RedirectView):

    url = reverse_lazy('users:auth_page_url')

    def post(self, request, *args, **kwargs):
        self.request.user.delete()
        logout(request)
        return super().post(request, *args, **kwargs)


class GetTokenView(RedirectView):
    url = reverse_lazy('users_cabinet:profile_settings_url')

    def post(self, request, *args, **kwargs):
        user = request.user
        login = user.login_ke
        password = user.pass_ke
        new_token.delay(login, password)
        messages.success(request, 'Получаем токен...')
        return super().post(request, *args, **kwargs)


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('main_app:main_page_url')


class DeleteStoreView(RedirectView):
    url = reverse_lazy('users_cabinet:profile_settings_url')

    def get(self, request, *args, **kwargs):
        Stores.objects.get(id=kwargs['store_id']).delete()
        return super().get(request, *args, **kwargs)


class ManagerStoreView(RedirectView):
    url = reverse_lazy('users_cabinet:profile_settings_url')

    def get(self, request, *args, **kwargs):
        action = kwargs['action']
        store_id = kwargs['store_id']
        parser_manager.delay(action, store_id)
        return super().get(self, request, *args, **kwargs)
