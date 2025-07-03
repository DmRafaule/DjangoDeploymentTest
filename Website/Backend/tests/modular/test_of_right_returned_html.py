from django.test import LiveServerTestCase
from django.core.files.base import ContentFile

from Backend.models import Post, Tag, Media
from Website.settings import STAGING_SERVER


class RightHTMLTest( LiveServerTestCase):
    def setUp(self):
        # Создаём записи в БД для Post, Tag и Media моделей
        self.post = Post()
        self.post.save()
        self.tag = Tag(slug='tag-1')
        self.tag.save()
        file = ContentFile("CONTENT", 'file.txt')
        self.media = Media(name='file one', file=file)
        self.media.save()

    def test_post_returned_right_html(self):
        ''' Тест на правильно возвращаемый шаблон для формы создания постов '''
        if STAGING_SERVER:
            SERVER_URL = STAGING_SERVER
        else:
            SERVER_URL = self.live_server_url
        response = self.client.get(f"{SERVER_URL}/en/api/get_post_form/{self.post.pk}")
        self.assertTemplateUsed(response, 'Backend/Parts/post.html')

    def test_tag_returned_right_html(self):
        ''' Тест на правильно возвращаемый шаблон для формы создания тегов '''
        if STAGING_SERVER:
            SERVER_URL = STAGING_SERVER
        else:
            SERVER_URL = self.live_server_url
        response = self.client.get(f"{SERVER_URL}/en/api/get_tag_form/{self.tag.pk}")
        self.assertTemplateUsed(response, 'Backend/Parts/tag.html')

    def test_media_returned_right_html(self):
        ''' Тест на правильно возвращаемый шаблон для формы создания тегов '''
        if STAGING_SERVER:
            SERVER_URL = STAGING_SERVER
        else:
            SERVER_URL = self.live_server_url
        response = self.client.get(f"{SERVER_URL}/en/api/get_media_form/{self.media.pk}")
        self.assertTemplateUsed(response, 'Backend/Parts/media.html')