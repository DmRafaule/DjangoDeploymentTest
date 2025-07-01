from django.urls import path

from .views import HomeView
from .views import EmailTestView
from .views import DatabaseTestView
from .views import MediaTestView
from .views import StaticTestView
from .views import TestingTestView
from .views import TranslationTestView, get_server_strings

urlpatterns = [
    path('', HomeView.as_view(), name='domashnyaya'),
    path('test-mail/', EmailTestView.as_view(), name='test-mail'),
    path('test-database/', DatabaseTestView.as_view(), name='test-database'),
    path('test-media/', MediaTestView.as_view(), name='test-media'),
    path('test-static/', StaticTestView.as_view(), name='test-static'),
    path('test-testing/', TestingTestView.as_view(), name='test-testing'),
    path('test-translation/', TranslationTestView.as_view(), name='test-translation'),
    path('test-translation/get-server-strings/', get_server_strings),
]
