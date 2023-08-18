from django.test import TestCase
from django.urls import reverse

from users.models import User


class UserAuthRegisterTestCace(TestCase):
    """Авторизация и регистрация пользователей"""

    def test_auth_page(self):
        """Страница авторизации"""
        response = self.client.get(reverse('users:auth_page_url'))

        self.assertEqual(response.status_code, 200)
        self.assertIn(response.context_data.get('title'), 'Авторизация пользователей')

    def test_reg_page(self):
        """Страница регистрации"""
        response = self.client.get(reverse('users:reg_page_url'))

        self.assertEqual(response.status_code, 200)
        self.assertIn(response.context_data.get('title'), 'Регистрация пользователей')

    def test_auth_true(self):
        """Успешная авторизация"""
        username = 'testuser'
        password = 'testPASS123'
        user = User.objects.create_user(username=username, password=password)
        response = self.client.post(reverse('rest:auth'), data={
            'username': user.username,
            'password': password
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(user.is_authenticated)

    def test_auth_false(self):
        """Неудачная авторизация. Пользователя не существует"""
        username = 'test_user'
        password = '11111'
        response = self.client.post(reverse('rest:auth'), data={
            'username': username,
            'password': password
        })
        self.assertEqual(response.status_code, 401)

    def test_reg_true(self):
        """Успешная регистрация"""
        username = 'test_user'
        password = 'testPASS123'
        response = self.client.post(reverse('rest:register'), data={
            'username': username,
            'password': password,
        })
        new_user = User.objects.get(username=username)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(new_user.username, username)
        self.assertTrue(new_user.is_authenticated)

    def test_reg_false(self):
        """Неудачная регистрация. Пользователь уже существует"""
        username = 'test_user'
        password = '11111'
        User.objects.create_user(username=username, password=password)
        response = self.client.post(reverse('rest:register'), data={
            'username': username,
            'password1': password,
            'password2': password,
        })

        self.assertEqual(response.status_code, 400)
