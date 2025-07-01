from django.urls import path

from .views import PostListView, TagListView, MediaListView, PostDetailedView, TagDetailedView, MediaDetailedView, get_post_form, get_tag_form, get_media_form
from .serializers import PostSerializer, TagSerializer, MediaSerializer
from .models import Post, Tag, Media


urlpatterns = [
    path('api/posts/', PostListView.as_view(serializer_class=PostSerializer, queryset=Post.objects.all()), name="posts"),
    path('api/tags/', TagListView.as_view(serializer_class=TagSerializer, queryset=Tag.objects.all()), name="tags"),
    path('api/medias/', MediaListView.as_view(serializer_class=MediaSerializer, queryset=Media.objects.all()), name="medias"),

    path('api/posts/<int:pk>', PostDetailedView.as_view(serializer_class=PostSerializer, queryset=Post.objects.all())),
    path('api/tags/<int:pk>', TagDetailedView.as_view(serializer_class=TagSerializer, queryset=Tag.objects.all())),
    path('api/medias/<int:pk>', MediaDetailedView.as_view(serializer_class=MediaSerializer, queryset=Media.objects.all())),

    path('api/get_post_form/<int:pk>', get_post_form),
    path('api/get_tag_form/<int:pk>', get_tag_form),
    path('api/get_media_form/<int:pk>', get_media_form)
]
