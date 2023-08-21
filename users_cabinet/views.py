from django.views.generic.list import ListView
from django.views.generic.base import RedirectView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import logout
from django.urls import reverse_lazy
from django.utils import timezone

from users_cabinet.models import ProductData, Stores, Reviews

from common.title import TitleMixin


class SettingsView(TitleMixin, SuccessMessageMixin, ListView):
    """Страница настроек"""
    template_name = 'users_cabinet/settings.html'
    title = 'Настройки'
    model = Stores
    success_message = 'Данные обновлены'
    success_url = reverse_lazy('users_cabinet:profile_settings_url')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stores'] = Stores.objects.filter(user=self.request.user.pk)
        return context


class ParserView(TitleMixin, ListView):
    """Страница парсинга"""
    template_name = 'users_cabinet/parser.html'
    title = 'Парсер'
    model = ProductData
    paginate_by = 40

    def get_queryset(self):
        queryset = super().get_queryset()
        selected_store = self.request.GET.get('store-select')
        select_period = int(self.request.GET.get('period-select', 1))
        time_delta = timezone.now() - timezone.timedelta(days=select_period)
        if not selected_store:  # Если не выбран магазин
            queryset = queryset.filter(store__user__username=self.request.user, datetime__gte=time_delta).order_by(
                '-datetime')
        elif selected_store:  # Если выбран магазин
            queryset = queryset.filter(store__store_name=selected_store, user__username=self.request.user,
                                       datetime__gte=time_delta).order_by('-datetime')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['period'] = int(self.request.GET.get('period-select', 1))
        context['selected_store'] = self.request.GET.get('store-select')
        context['time_interval'] = [i for i in range(1, 8)]
        context['store_data'] = Stores.objects.filter(user__username=self.request.user)
        return context


class ReviewsView(TitleMixin, ListView):
    """Страница с отзывами"""
    template_name = 'users_cabinet/reviews.html'
    title = 'Отзывы'
    model = Reviews

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.request.user.token:
            context['token_message'] = 'Необходимо добавить данные для авторизации в настройках'
        elif not self.request.user.token_valid:
            context['token_message'] = 'Необходимо заменить токен авторизации в настройках'
        return context


class DeleteProfileView(RedirectView):
    """Удалить профиль"""
    url = reverse_lazy('users:auth_page_url')

    def post(self, request, *args, **kwargs):
        self.request.user.delete()
        logout(request)
        return super().post(request, *args, **kwargs)


