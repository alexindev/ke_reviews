from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework import status

from django.contrib.auth import authenticate, login
from django.db import IntegrityError

from rest.serializers import ReviewSerializer
from rest.tasks import new_token, get_reviews
from rest.utils.stores import get_store
from rest.utils.paginate import ReviewsPaginate

from celery.result import AsyncResult
from users.models import User
from users_cabinet.models import Stores, Reviews


class UserAuthView(APIView):
    """Авторизация пользователей"""
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return Response(status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Проверьте корректность логина и пароля'}, status=status.HTTP_401_UNAUTHORIZED)


class UserRegisterView(APIView):
    """Регистрация поьзователей"""
    def post(self, request):
        try:
            username = request.data.get('username')
            password = request.data.get('password')
            User.objects.create_user(username=username, password=password)
            return Response(status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response({'message': 'Пользователь с таким именем уже зарегистрирован'},
                            status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'message': e}, status=status.HTTP_400_BAD_REQUEST)


class ReviewsShowView(ListAPIView):
    """Вывывести все отзывы"""
    serializer_class = ReviewSerializer
    pagination_class = ReviewsPaginate

    def get_queryset(self):
        user = User.objects.get(id=self.request.user.pk)
        queryset = Reviews.objects.filter(user=user).order_by('-date_create')
        return queryset


class ReviewsUpdateView(APIView):
    """Обновить отзывы"""
    def get(self, request):
        user = User.objects.get(id=request.user.pk)
        get_reviews.delay(user.token, user.pk)
        return Response({'message': 'Получаем обновления', 'status': True})


class DeleteStoreView(APIView):
    """Удалить магазин"""
    def delete(self, request):
        store_id = request.data.get('store_id')
        if store_id:
            store = Stores.objects.get(id=store_id)
            if store:
                store.delete()
                return Response({'message': f'Магазин {store} удален', 'status': True})
            else:
                return Response({'message': 'Магазин не найден', 'status': False})
        else:
            return Response({'message': 'Ошибка удаления магазина', 'status': False})


class UpdateStoreStatusView(APIView):
    """Обновить статус магазина"""
    def put(self, request):
        store_id = request.data.get('store_id')
        store_status = request.data.get('store_status')
        if store_id and store_status:
            store_status = False if store_status == 'True' else True
            store = Stores.objects.get(id=store_id)
            store.status = store_status
            store.save()
            return Response({'message': f'{store_status}', 'status': True})
        else:
            return Response({'message': 'Не корректное переключение статуса', 'status': False})


class NewStoreView(APIView):
    """Добавить новый магазин"""
    def post(self, request):
        store_url: str = request.data.get('new_store').strip()
        store_name = store_url.split('/')[-1]
        if store_url:
            if not Stores.objects.filter(user=request.user, store_url=store_url).exists():
                if get_store(store_url):
                    store = Stores.objects.create(store_url=store_url, store_name=store_name, user=request.user)
                    return Response(
                        {'message': f'Магазин {store_name} успешно добавлен', 'store_id': store.id, 'status': True})
                else:
                    return Response({'message': f'{store_name} - данного магазина не существует', 'status': False})
            else:
                return Response({'message': f'Магазин {store_name} уже добавлен', 'status': False})
        else:
            return Response({'message': 'Введите ссылку на магазин', 'status': False})


class ReviewSettingsView(APIView):
    """Добавить/обновить данные учетной записи для отзывов"""
    def put(self, request):
        login = request.data.get('login')
        password = request.data.get('password')
        if login and password:
            user_data, created = User.objects.update_or_create(
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
        else:
            return Response({'message': 'Необходимо заполнить все поля', 'status': False})


class UserPicView(APIView):
    """Добавить/изменить аватар пользователя"""
    def post(self, request):
        picture = request.data.get('picture')
        if picture:
            user_data, created = User.objects.update_or_create(
                id=request.user.pk,
                defaults={
                    'image': picture
                }
            )
            if created:
                return Response({'message': 'Аватар добавлен', 'status': True})
            else:
                return Response({'message': 'Аватар обновлен', 'status': True})
        else:
            return Response({'message': 'Добавьте изображение', 'status': False})


class GetNewTokenView(APIView):
    """Получить новый токен для отзывов"""
    def get(self, request):
        user = User.objects.get(id=request.user.pk)
        login_ke = user.login_ke
        pass_ke = user.pass_ke

        if not login_ke or not pass_ke:
            return Response({'message': 'Логин и/или пароль не добавлены', 'status': False})

        task = new_token.delay(request.user.pk, login_ke, pass_ke)
        return Response({'message': 'Получаем токен...', 'task_id': task.id, 'status': True})


class GetTaskStatusView(APIView):
    """Проверка статуса таска"""
    def get(self, request):
        task_id = request.GET.get('task_id')
        if not task_id:
            return Response({'message': 'Task ID не задан', 'status': False})

        task = AsyncResult(task_id)
        if task.state == 'SUCCESS':
            result = task.result
            if result:
                return Response({'message': 'Задача выполнена успешно', 'token': result, 'status': True})
            else:
                return Response({'message': 'Задача завершилась неудачно', 'status': False})
        elif task.state == 'PENDING' or task.state == 'STARTED':
            return Response({'message': 'Выполняется текущая задача...', 'status': True})
        else:
            return Response({'message': 'Ошибка при выполнении задачи', 'status': False})

