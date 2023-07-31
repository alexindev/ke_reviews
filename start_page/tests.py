from django.test import TestCase
from django.urls import reverse

from users.models import User


class StartPageTestCase(TestCase):

    def test_load_start_page(self):
        """Загрузка стартовой страницы"""
        response = self.client.get(reverse('start_page:start_page_url'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(response.context_data.get('title'), 'Главная страница')

    def test_404_page(self):
        """Страница 404"""
        response = self.client.get('/page/that/does/not/exist/')
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, 'page404.html')

    def test_logout(self):
        """Разлогиниться с главной страницы"""
        username = 'testuser'
        password = 'testPASS123'
        url = reverse('start_page:logout_url')
        user = User.objects.create(username=username, password=password)
        self.client.login(username=username, password=password)
        self.assertTrue(user.is_authenticated)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('users:auth_page_url'), response.url)
        self.assertFalse(response.wsgi_request.user.is_authenticated)


