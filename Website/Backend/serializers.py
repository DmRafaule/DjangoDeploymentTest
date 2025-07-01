from rest_framework import serializers
from .models import Post, Tag, Media

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('__all__')

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('__all__')

class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = ('__all__')