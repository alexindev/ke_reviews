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

