from django.test import LiveServerTestCase, RequestFactory
from django.core.files.base import ContentFile
from django.middleware.csrf import get_token

from rest_framework import generics, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.test import APIClient

from Backend.models import Post, Tag, Media
from Backend.views import PostListView, TagListView, MediaListView
from Backend.serializers import PostSerializer, TagSerializer, MediaSerializer
from Website.settings import STAGING_SERVER


class ListViewTest(LiveServerTestCase):
    ''' Тестирует работу представлений  '''
    def setUp(self):
        # Создаём соответствующие представление класс PostDetailedView
        ## Создаём пост (Post)
        self.post = Post()
        self.post.save()
        self.post.save()
        self.post.save()
        # Создаём соответствующие представление класс TagDetailedView
        ## Создаём тег (Tag)
        self.tag1 = Tag(slug='tag-1')
        self.tag1.save()
        self.tag2 = Tag(slug='tag-2')
        self.tag2.save()
        self.tag3 = Tag(slug='tag-3')
        self.tag3.save()
        # Создаём соответствующие представление класс TagDetailedView
        ## Создаём тег (Tag)
        file = ContentFile("CONTENT", 'file.txt')
        self.media = Media(name='file one', file=file)
        self.media.save()
        self.media = Media(name='file one', file=file)
        self.media.save()
        self.media = Media(name='file one', file=file)
        self.media.save()
    
    def test_get_request_for_posts(self):
        ''' Проверяем работу GET запроса, получение списка постов '''
        if STAGING_SERVER:
            SERVER_URL = STAGING_SERVER
        else:
            SERVER_URL = self.live_server_url
        client = APIClient()
        # Проверка пагинации для постов
        response = client.get(f'{SERVER_URL}/en/api/posts/?page=1&limit=4')
        self.assertEqual(len(response.data.get('posts')), len(Post.objects.all()))
    
    def test_get_request_for_tags(self):
        ''' Проверяем работу GET запроса, получение списка тегов '''
        if STAGING_SERVER:
            SERVER_URL = STAGING_SERVER
        else:
            SERVER_URL = self.live_server_url
        client = APIClient()
        # Проверка пагинации для тегов
        response = client.get(f'{SERVER_URL}/en/api/tags/?page=1&limit=4')
        self.assertEqual(len(response.data.get('posts')), len(Tag.objects.all()))
    
    def test_get_request_for_medias(self):
        ''' Проверяем работу GET запроса, получение списка медиа '''
        if STAGING_SERVER:
            SERVER_URL = STAGING_SERVER
        else:
            SERVER_URL = self.live_server_url
        client = APIClient()
        # Проверка пагинации для медиа
        response = client.get(f'{SERVER_URL}/en/api/medias/?page=1&limit=4')
        self.assertEqual(len(response.data.get('posts')), len(Media.objects.all()))
    
    def test_post_request_for_posts(self):
        ''' Проверяем работу POST запроса, добавление поста элемента '''
        if STAGING_SERVER:
            SERVER_URL = STAGING_SERVER
        else:
            SERVER_URL = self.live_server_url
        client = APIClient()
        # Проверка правильной отправленной формы для создания поста
        response = client.post(
            f'{SERVER_URL}/en/api/posts/',
            data = {
                "tags": [],
                "title": "New title",
                "description": "New descr",
                "note": "New note",
            })
        self.assertIs(response.status_code, status.HTTP_201_CREATED )
        # Проверка не правильной отправленной формы для создания поста
        response = client.post(
            f'{SERVER_URL}/en/api/posts/',
            data = {
                "tags": [],
                "description": "New descr",
                "note": "New note",
            })
        self.assertIs(response.status_code, status.HTTP_204_NO_CONTENT )

    def test_post_request_for_tags(self):
        ''' Проверяем работу POST запроса, добавление нового тега '''
        if STAGING_SERVER:
            SERVER_URL = STAGING_SERVER
        else:
            SERVER_URL = self.live_server_url
        client = APIClient()
        # Проверка правильной отправленной формы для создания тега
        response = client.post(
            f'{SERVER_URL}/en/api/tags/',
            data = {
                "name": "New name",
                "slug": "new-slug",
            })
        self.assertIs(response.status_code, status.HTTP_201_CREATED )
        # Проверка не правильной отправленной формы для создания тега
        response = client.post(
            f'{SERVER_URL}/en/api/tags/',
            data = {
                "name": "New name",
            })
        self.assertIs(response.status_code, status.HTTP_204_NO_CONTENT )

    def test_post_request_for_medias(self):
        ''' Проверяем работу POST запроса, добавление нового медиа '''
        if STAGING_SERVER:
            SERVER_URL = STAGING_SERVER
        else:
            SERVER_URL = self.live_server_url
        client = APIClient()
        # Проверка правильной отправленной формы для создания медиа
        new_file = ContentFile("CONTENT", 'file_new.txt')
        response = client.post(
            f'{SERVER_URL}/en/api/medias/',
            data = {
                "name": "New-name",
                "file": new_file
            })
        self.assertIs(response.status_code, status.HTTP_201_CREATED )
        # Проверка не правильной отправленной формы для создания медиа
        response = client.post(
            f'{SERVER_URL}/en/api/medias/',
            data = {
                "name": "New-name",
            })
        self.assertIs(response.status_code, status.HTTP_400_BAD_REQUEST )