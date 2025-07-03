from django.test import LiveServerTestCase, RequestFactory
from django.core.files.base import ContentFile
from django.middleware.csrf import get_token

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.test import APIClient

from Backend.models import Post, Tag, Media
from Backend.views import PostDetailedView, TagDetailedView, MediaDetailedView
from Backend.serializers import PostSerializer, TagSerializer, MediaSerializer


class DetailedViewTest(LiveServerTestCase):
    def setUp(self):
        # Создаём соответствующие представление класс PostDetailedView
        ## Создаём пост (Post)
        self.post = Post()
        self.post.save()
        ## Конструируем класс-представление
        self.post_detailed_view = PostDetailedView()
        self.post_detailed_view.queryset = Post.objects.all()
        self.post_detailed_view.serializer_class = PostSerializer
        self.post_detailed_view.kwargs = {'pk': self.post.pk}
        # Создаём соответствующие представление класс TagDetailedView
        ## Создаём тег (Tag)
        self.tag = Tag(slug='tag-1')
        self.tag.save()
        ## Конструируем класс-представление
        self.tag_detailed_view = TagDetailedView()
        self.tag_detailed_view.queryset = Tag.objects.all()
        self.tag_detailed_view.serializer_class = TagSerializer
        self.tag_detailed_view.kwargs = {'pk': self.tag.pk}
        # Создаём соответствующие представление класс TagDetailedView
        ## Создаём тег (Tag)
        file = ContentFile("CONTENT", 'file.txt')
        self.media = Media(name='file one', file=file)
        self.media.save()
        ## Конструируем класс-представление
        self.media_detailed_view = MediaDetailedView()
        self.media_detailed_view.queryset = Media.objects.all()
        self.media_detailed_view.serializer_class = MediaSerializer
        self.media_detailed_view.kwargs = {'pk': self.media.pk}

    def test_get_request(self):
        ''' Проверяем работу GET запроса '''
        ## Конструируем запрос для поста
        get_posts_django_request = RequestFactory().get(f"{self.live_server_url}/en/api/posts/{self.post.pk}")
        get_posts_request = Request(get_posts_django_request)
        self.post_detailed_view.request = get_posts_request
        inst: Response = self.post_detailed_view.get(get_posts_request)
        self.assertIsInstance(inst.data.get('post'), Post)
        ## Конструируем запрос для тега
        get_tags_django_request = RequestFactory().get(f"{self.live_server_url}/en/api/tags/{self.tag.pk}")
        get_tags_request = Request(get_tags_django_request)
        self.tag_detailed_view.request = get_tags_request
        inst: Response = self.tag_detailed_view.get(get_tags_request)
        self.assertIsInstance(inst.data.get('post'), Tag)
        ## Конструируем запрос для медиа
        get_medias_django_request = RequestFactory().get(f"{self.live_server_url}/en/api/medias/{self.media.pk}")
        get_medias_request = Request(get_medias_django_request)
        self.media_detailed_view.request = get_medias_request
        inst: Response = self.media_detailed_view.get(get_medias_request)
        self.assertIsInstance(inst.data.get('post'), Media)

    def test_delete_request(self):
        ''' Проверяем работу DELETE запроса '''
        ## Конструируем запрос для поста
        delete_posts_django_request = RequestFactory().delete(f"{self.live_server_url}/en/api/posts/{self.post.pk}")
        delete_posts_request = Request(delete_posts_django_request)
        self.post_detailed_view.request = delete_posts_request
        inst: Response = self.post_detailed_view.delete(delete_posts_request)
        self.assertTrue(inst.data.get('is_delete'))
        ## Конструируем запрос для тега
        delete_tags_django_request = RequestFactory().delete(f"{self.live_server_url}/en/api/tags/{self.tag.pk}")
        delete_tags_request = Request(delete_tags_django_request)
        self.tag_detailed_view.request = delete_tags_request
        inst: Response = self.tag_detailed_view.delete(delete_tags_request)
        self.assertTrue(inst.data.get('is_delete'))
        ## Конструируем запрос для медиа
        delete_medias_django_request = RequestFactory().delete(f"{self.live_server_url}/en/api/medias/{self.media.pk}")
        delete_medias_request = Request(delete_medias_django_request)
        self.media_detailed_view.request = delete_medias_request
        inst: Response = self.media_detailed_view.delete(delete_medias_request)
        self.assertTrue(inst.data.get('is_delete'))
    
    def test_put_request(self):
        ''' Проверяем работу PUT запроса '''
        client = APIClient()
        ## Конструируем запрос для поста
        post_before_pk = self.post.pk
        post_before_title = self.post.title
        client.put(f"{self.live_server_url}/en/api/posts/{self.post.pk}", 
            data={
                "tags": [],
                "title": "New title",
                "description": "New descr",
                "note": "New note",
            })
        self.post.refresh_from_db()
        self.assertEqual(post_before_pk, self.post.pk)
        self.assertNotEqual(post_before_title, self.post.title)
        ## Конструируем запрос для тега
        tag_before_pk = self.tag.pk
        tag_before_name = self.tag.name
        client.put(f"{self.live_server_url}/en/api/tags/{self.tag.pk}", 
            data={
                "name": "New name",
                "slug": "new-slug",
            })
        self.tag.refresh_from_db()
        self.assertEqual(tag_before_pk, self.tag.pk)
        self.assertNotEqual(tag_before_name, self.tag.name)
        ## Конструируем запрос для тега
        media_before_pk = self.media.pk
        media_before_name = self.media.name
        new_file = ContentFile("CONTENT", 'file_new.txt')
        client.put(f"{self.live_server_url}/en/api/medias/{self.media.pk}", 
            data={
                "name": "New-name",
                "file": new_file
            })
        self.media.refresh_from_db()
        self.assertEqual(media_before_pk, self.media.pk)
        self.assertNotEqual(media_before_name, self.media.name)