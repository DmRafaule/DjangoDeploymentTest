from django.urls import path

from .views import BaseView
from .views import EmailTestView
from .views import get_server_strings

urlpatterns = [
    path('', BaseView.as_view(template_name="domashnyaya.html"), name='domashnyaya'),
    path('test-mail/', EmailTestView.as_view(), name='test-mail'),
    path('test-database/', BaseView.as_view(template_name="test-database.html"), name='test-database'),
    path('test-media/', BaseView.as_view(template_name="test-media.html"), name='test-media'),
    path('test-static/', BaseView.as_view(template_name="test-static.html"), name='test-static'),
    path('test-testing/', BaseView.as_view(template_name="test-testing.html"), name='test-testing'),
    path('test-translation/', BaseView.as_view(template_name="test-translation.html"), name='test-translation'),
    path('test-translation/get-server-strings/', get_server_strings),
]
