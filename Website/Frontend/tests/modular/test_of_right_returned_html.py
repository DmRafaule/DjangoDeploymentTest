from django.urls import reverse
from django.test import LiveServerTestCase
from django.core.files.base import ContentFile

from Backend.models import Post, Tag, Media


class RightHTMLTest( LiveServerTestCase):

    def test_home_returned_right_html(self):
        ''' Тест на правильно возвращаемый шаблон для домашней страницы '''
        response = self.client.get(reverse('domashnyaya'))
        self.assertTemplateUsed(response, 'domashnyaya.html')

    def test_mail_returned_right_html(self):
        ''' Тест на правильно возвращаемый шаблон для страницы проверки отправки почты'''
        response = self.client.get(reverse('test-mail'))
        self.assertTemplateUsed(response, 'test-mail.html')

    def test_database_returned_right_html(self):
        ''' Тест на правильно возвращаемый шаблон для страницы проверки базы данных '''
        response = self.client.get(reverse('test-database'))
        self.assertTemplateUsed(response, 'test-database.html')

    def test_media_returned_right_html(self):
        ''' Тест на правильно возвращаемый шаблон для страницы проверки медиа'''
        response = self.client.get(reverse('test-media'))
        self.assertTemplateUsed(response, 'test-media.html')

    def test_static_returned_right_html(self):
        ''' Тест на правильно возвращаемый шаблон для страницы проверки статики'''
        response = self.client.get(reverse('test-static'))
        self.assertTemplateUsed(response, 'test-static.html')

    def test_testing_returned_right_html(self):
        ''' Тест на правильно возвращаемый шаблон для страницы проверки тестирования '''
        response = self.client.get(reverse('test-testing'))
        self.assertTemplateUsed(response, 'test-testing.html')

    def test_translation_returned_right_html(self):
        ''' Тест на правильно возвращаемый шаблон для страницы проверки переводов '''
        response = self.client.get(reverse('test-translation'))
        self.assertTemplateUsed(response, 'test-translation.html')