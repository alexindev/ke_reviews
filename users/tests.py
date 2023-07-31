from django.test import TestCase
from django.urls import reverse

from users.models import User


class UserAuthRegisterTestCace(TestCase):
    """Авторизация и регистрация пользователей"""

    @classmethod
    def setUpTestData(cls):
        cls.auth_page = reverse('users:auth_page_url')
        cls.reg_page = reverse('users:reg_page_url')

    def test_auth_page(self):
        """Страница авторизации"""
        response = self.client.get(self.auth_page)
        self.assertEqual(response.status_code, 200)
        self.assertIn(response.context_data.get('title'), 'Авторизация пользователей')

    def test_auth_false(self):
        """Неудачная авторизация"""
        username = 'test_user'
        password = '11111'
        response = self.client.post(self.auth_page, data={
            'username': username,
            'password': password
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context_data.get('form').error_messages)

    def test_auth_true(self):
        """Успешная авторизация"""
        username = 'testuser'
        password = 'testPASS123'
        user = User.objects.create_user(username=username, password=password)
        response = self.client.post(self.auth_page, data={
            'username': user.username,
            'password': password
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(user.is_authenticated)
        self.assertEqual(response.url, reverse('users_cabinet:users_profile_url'))

    def test_reg_page(self):
        """Страница регистрации"""
        response = self.client.get(self.reg_page)
        self.assertEqual(response.status_code, 200)
        self.assertIn(response.context_data.get('title'), 'Регистрация пользователей')

    def test_reg_false(self):
        """Неудачная регистрация"""
        username = 'test_user'
        password = '11111'
        response = self.client.post(self.reg_page, data={
            'username': username,
            'password1': password,
            'password2': password,
        })

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context_data.get('form').error_messages)

    def test_reg_true(self):
        """Успешная регистрация"""
        username = 'test_user'
        password = 'testPASS123'
        response = self.client.post(self.reg_page, data={
            'username': username,
            'password1': password,
            'password2': password,
        })

        new_user = User.objects.get(username=username)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('users:auth_page_url'))
        self.assertEqual(new_user.username, username)
        self.assertTrue(new_user.is_authenticated)
