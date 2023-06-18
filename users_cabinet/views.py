from django.views.generic.list import ListView
from django.views.generic.edit import FormView
from django.contrib.auth.views import LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy

from users.models import Users
from .models import UserStores

from common.title import TitleMixin
from .forms import UserPicForm, UserDataForm, StoreForm


class ProfileView(TitleMixin, ListView):
    template_name = 'users_cabinet/profile.html'
    model = Users
    title = 'Главное меню'


class SettingsView(TitleMixin, SuccessMessageMixin, FormView):
    template_name = 'users_cabinet/settings.html'
    title = 'Настройки'
    form_class = UserPicForm
    success_message = 'Данные обновлены'
    success_url = reverse_lazy('users_cabinet:profile_settings_url')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['avatar_form'] = UserPicForm(instance=self.request.user)
        context['user_data_form'] = UserDataForm(instance=self.request.user)
        context['store_form'] = StoreForm()
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
                store = store_form.save()
                UserStores.objects.create(store=store, user=self.request.user)

        return super().form_valid(form)


class ParserView(TitleMixin, ListView):
    template_name = 'users_cabinet/parser.html'
    model = Users
    title = 'Парсер'


class ReviewsView(TitleMixin, ListView):
    template_name = 'users_cabinet/reviews.html'
    model = Users
    title = 'Отзывы'


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('main_app:main_page_url')

