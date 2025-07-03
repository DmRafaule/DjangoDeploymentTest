from django.test import LiveServerTestCase, RequestFactory
from django.core.files.base import ContentFile

from rest_framework.request import Request

from Backend.models import Post, Tag, Media
from Backend.views import PostListView
from Backend.serializers import PostSerializer


class FiltrationTest(LiveServerTestCase):
    def setUp(self):
        # Создаём записи в БД для Post, Tag и Media моделей
        self.tag1 = Tag(slug='tag-1')
        self.tag1.save()
        self.tag2 = Tag(slug='tag-2')
        self.tag2.save()
        self.post1 = Post()
        self.post1.save()
        self.post1.tags.add(self.tag1)
        self.post1.tags.add(self.tag2)
        self.post2 = Post()
        self.post2.save()
        self.post2.tags.add(self.tag1)

    
    def test_tag_filtration_for_post(self):
        ''' Проверка на правильность фильтрации по тегам '''
        # Конструируем запрос
        django_request = RequestFactory().get(f"{self.live_server_url}/en/api/posts/?page=1&limit=4&tag=tag-2")
        request = Request(django_request)
        # Конструируем класс-представление
        cl_view = PostListView()
        cl_view.request = request
        cl_view.queryset = Post.objects.all()
        cl_view.serializer_class = PostSerializer
        queryset = cl_view.get_queryset()
        # Проверяем
        self.assertIn(self.post1, queryset)
        self.assertNotIn(self.post2, queryset)
