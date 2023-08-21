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
        Stores.objects.create(store_url=store_url, store_name=store_name, user=self.user)
        data = {'new_store': store_url}

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
        store_url = 'https://kazanexpress.ru/kazanexpress'
        self.user = User.objects.create_user(username=username, password=password)
        self.client.login(username=username, password=password)
        Stores.objects.create(user=self.user, store_url=store_url)

    def test_update_store_status_success(self):
        """
        Успешная смана статуса магазина
        Статус код 202
        """
        url = reverse('rest:store_status')
        data = {'store_id': self.user.pk, 'store_status': 'False'}
        response = self.client.put(path=url, data=data, content_type='application/json')
        self.assertEqual(response.data.get('message'), True)
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

    def test_update_store_status_nok(self):
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

