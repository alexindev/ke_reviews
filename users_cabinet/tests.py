from django.test import TestCase
from django.shortcuts import reverse

from rest_framework import status

from users.models import User
from users_cabinet.models import Stores


class NewStoreTestCase(TestCase):
    def setUp(self):
        """
        Инициализация перед каждым тестом
        Добавление пользователя. Создание клиента
        """
        username = 'testuser'
        password = 'testpassword'
        self.user = User.objects.create_user(username=username, password=password)
        self.client.login(username=username, password=password)
        self.url = reverse('rest:new_store')

    def test_empty_input(self):
        """
        Проверка ввода данных.
        При пустом значении выводит соответствующее сообщение
        Статус код 405
        """
        url = reverse('rest:new_store')
        data = {'new_store': ''}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response.data.get('message'), 'Введите ссылку на магазин')

    def test_succes_add_store(self):
        """
        Успешное добавление магазина
        Статус код 201
        """
        store_name = 'kazanexpress'
        data = {'new_store': f'https://kazanexpress.ru/{store_name}'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('message'), f'Магазин {store_name} успешно добавлен')

    def test_not_correct_store(self):
        """
        Магазина не существует
        Статус код 404
        """
        store_name = 'stone_not_found'
        data = {'new_store': f'https://kazanexpress.ru/{store_name}'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data.get('message'), f'{store_name} - данного магазина не существует')

    def test_exists_store(self):
        """
        Магазин уже добавлен
        Статус код 400
        """
        store_name = 'kazanexpress'
        store_url = f'https://kazanexpress.ru/{store_name}'
        data = {'new_store': store_url}
        Stores.objects.create(store_url=store_url, store_name=store_name, user=self.user)

        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('message'), f'Магазин {store_name} уже добавлен')


class ManageStoreTestCase(TestCase):

    def setUp(self):
        """
        Инициализация перед каждым тестом
        Добавление пользователя. Создание клиента
        По умолчанию, после добавления магазина присваивается статус False
        """
        username = 'testuser'
        password = 'testpassword'
        self.store_name = 'kazanexpress'
        store_url = f'https://kazanexpress.ru/{self.store_name}'
        self.user = User.objects.create_user(username=username, password=password)
        self.client.login(username=username, password=password)
        self.store = Stores.objects.create(user=self.user, store_url=store_url, store_name=self.store_name)

    def test_update_store_status_success(self):
        """
        Успешная смана статуса магазина
        Статус код 202
        """
        url = reverse('rest:store_status')
        data = {'store_id': self.store.pk, 'store_status': 'False'}
        response = self.client.put(path=url, data=data, content_type='application/json')
        self.assertEqual(response.data.get('message'), 'True')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

    def test_update_store_status_fail(self):
        """
        Ошибка при смене статуса магазина.
        Не обнаружен магазин с заданным ID
        Статус код 404
        """
        url = reverse('rest:store_status')
        data = {'store_id': 100, 'store_status': 'False'}
        response = self.client.put(path=url, data=data, content_type='application/json')
        self.assertEqual(response.data.get('message'), 'Магазин не найден')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_store_status_bad(self):
        """
        Ошибка при смене статуса.
        Не передан ID магазина
        Статус код 400
        """
        url = reverse('rest:store_status')
        data = {'store_id': '', 'store_status': 'False'}
        response = self.client.put(path=url, data=data, content_type='application/json')
        self.assertEqual(response.data.get('message'), 'Не корректное переключение статуса')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_store_success(self):
        """
        Успешное удаление магазина
        Статус код 202
        """
        url = reverse('rest:delete_store')
        data = {'store_id': self.store.pk}
        response = self.client.delete(path=url, data=data, content_type='application/json')
        self.assertEqual(response.data.get('message'),  f'Магазин {self.store_name} удален')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

    def test_delete_store_fail(self):
        """
        Ошибка удаления магазина
        Магазин не найден в БД
        Статус код 404
        """
        url = reverse('rest:delete_store')
        data = {'store_id': 999}
        response = self.client.delete(path=url, data=data, content_type='application/json')
        self.assertEqual(response.data.get('message'), 'Магазин не найден')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_store_bad(self):
        """
        Ошибка удаления магазина
        Не передан store_id
        Статус код 400
        """
        url = reverse('rest:delete_store')
        data = {'store_id': ''}
        response = self.client.delete(path=url, data=data, content_type='application/json')
        self.assertEqual(response.data.get('message'), 'Ошибка удаления магазина')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ReviewSettingsTestCase(TestCase):
    def setUp(self):
        """
        Инициализация перед каждым тестом
        Добавление пользователя.
        """
        username = 'testuser'
        password = 'testpassword'
        self.url = reverse('rest:review')
        self.user = User.objects.create_user(username=username, password=password)
        self.client.login(username=username, password=password)

    def test_update_review_settings_success(self):
        """
        Успешное добавление данных для учетной записи
        Статус код 202
        """
        data = {'login': 'testlogin', 'password': 'testpassword'}
        response = self.client.put(path=self.url, data=data, content_type='application/json')
        self.assertEqual(response.data.get('message'), 'Данные учетной записи обновлены')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

    def test_upadate_review_setting_fail(self):
        """
        Ошибка при добавлении учетных данных.
        Не все поля заполнены
        Статус код 400
        """
        data = {'login': 'testlogin', 'password': ''}
        response = self.client.put(path=self.url, data=data, content_type='application/json')
        self.assertEqual(response.data.get('message'), 'Необходимо заполнить все поля')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserPicTestCase(TestCase):
    def setUp(self):
        """
        Инициализация перед каждым тестом
        Добавление пользователя.
        """
        username = 'testuser'
        password = 'testpassword'
        self.url = reverse('rest:avatar')
        self.user = User.objects.create_user(username=username, password=password)
        self.client.login(username=username, password=password)

    def test_change_userpic_success(self):
        """
        Успешная смена аватара пользователя
        Статус код 201
        """
        data = {'picture': b'new_image.jpg'}
        response = self.client.post(path=self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('message'), 'Аватар добавлен')

    def test_change_userpic_fail(self):
        """
        Ошибка при смене аватара
        Запрос без изображения
        Статус код 400
        """
        data = {'picture': b''}
        response = self.client.post(path=self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('message'), 'Добавьте изображение')


