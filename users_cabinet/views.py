from django.views.generic.list import ListView
from django.views.generic.base import RedirectView
from django.contrib.auth.views import LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import logout
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response

from users.models import Users
from users_cabinet.models import ProductData, Stores, Reviews

from common.title import TitleMixin
from users_cabinet.tasks import new_token, get_reviews
from users_cabinet.utils.stores import get_store


class ProfileView(TitleMixin, ListView):
    template_name = 'users_cabinet/profile.html'
    model = Users
    title = 'Главное меню'


class SettingsView(TitleMixin, SuccessMessageMixin, ListView):
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
            queryset = queryset.filter(store__user__username=self.request.user, datetime__gte=time_delta)
        elif selected_store:  # Если выбран магазин
            queryset = queryset.filter(store__store_name=selected_store, user__username=self.request.user,
                                       datetime__gte=time_delta)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['period'] = int(self.request.GET.get('period-select', 1))
        context['selected_store'] = self.request.GET.get('store-select')
        context['time_interval'] = [i for i in range(1, 8)]
        context['store_data'] = Stores.objects.filter(user__username=self.request.user)
        return context


class ReviewsView(TitleMixin, ListView):
    template_name = 'users_cabinet/reviews.html'
    title = 'Отзывы'
    model = Reviews
    ordering = '-date_create'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = Users.objects.get(id=self.request.user.pk)

        if not user.token:
            context['token_message'] = 'Необходимо добавить данные для авторизации в настройках'
        elif user.token_valid is False:
            context['token_message'] = 'Необходимо заменить токен авторизации в настройках'
        return context

    def get_queryset(self):
        queryset = super().get_queryset().filter(user=self.request.user)
        return queryset

    def post(self, request, *args, **kwargs):
        user = Users.objects.get(id=request.user.pk)
        token = user.token
        user_pk = user.pk
        get_reviews.delay(token, user_pk)
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
    next_page = reverse_lazy('start_page:main_page_url')


class DeleteStoreView(RedirectView):
    url = reverse_lazy('users_cabinet:profile_settings_url')

    def get(self, request, *args, **kwargs):
        Stores.objects.get(id=kwargs['store_id']).delete()
        return super().get(request, *args, **kwargs)


class UpdateStoreStatusView(APIView):
    """Обновить статус магазина"""
    def put(self, request, store_id):
        store_status = request.data.get('store_status')
        store_status = False if store_status == 'True' else True
        store = Stores.objects.get(id=store_id)
        store.status = store_status
        store.save()
        return Response({'store_status': f'{store_status}'})


class NewStoreView(APIView):
    """Добавить новый магазин"""
    def post(self, request):
        store_url: str = request.data.get('new_store').strip()
        store_name = store_url.split('/')[-1]

        if not Stores.objects.filter(user=request.user, store_url=store_url).exists():
            if get_store(store_url):
                Stores.objects.create(store_url=store_url, store_name=store_name, user=request.user)
                return Response({'message': f'Магазин {store_name} успешно добавлен', 'status': True})
            else:
                return Response({'message': f'{store_name} - данного магазина не существует', 'status': False})
        else:
            return Response({'message': f'Магазин {store_name} уже добавлен', 'status': False})


class ReviewDataView(APIView):
    """Добавить/обновить данные учетной записи для отзывов"""
    def put(self, request):
        login = request.data.get('login')
        password = request.data.get('password')
        user_data, created = Users.objects.update_or_create(
            id=request.user.pk,
            defaults={
                'login_ke': login,
                'pass_ke': password
            }
        )
        if created:
            return Response({'message': 'Учетная запись добавлена', 'status': True})
        else:
            return Response({'message': 'Данные учетной записи обновлены', 'status': True})


class UserPicView(APIView):
    """Добавить/изменить аватар пользователя"""
    def post(self, request):
        picture = request.data.get('picture')
        user_data, created = Users.objects.update_or_create(
            id=request.user.pk,
            defaults={
                'image': picture
            }
        )
        if created:
            return Response({'message': 'Аватар добавлен', 'status': True})
        else:
            return Response({'message': 'Аватар обновлен обновлены', 'status': True})

