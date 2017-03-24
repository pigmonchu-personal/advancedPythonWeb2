from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import serializers
from blogs.models import Blog, Category


class CategoriesListSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    name = serializers.CharField()
    description = serializers.CharField()


class BlogsListSerializer(serializers.Serializer):

    id = serializers.ReadOnlyField()
    name = serializers.CharField()
    description = serializers.CharField()
    owner = serializers.CharField()
    url = serializers.SerializerMethodField()

    def get_url(self, obj):
        return reverse('blog_detail', args=[obj.id])
