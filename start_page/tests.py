from django.test import TestCase
from django.urls import reverse

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
