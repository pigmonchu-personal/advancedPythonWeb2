from rest_framework import serializers

from blogs.models import Blog


class BlogsListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Blog
        fields = ("id", "name", "description", "owner")