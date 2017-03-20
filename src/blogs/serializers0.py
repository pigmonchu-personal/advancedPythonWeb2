from django.contrib.auth.models import User
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
