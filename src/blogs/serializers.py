from rest_framework import serializers

from blogs.models import Blog, Post


class BlogsListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Blog
        fields = ("id", "name", "description", "owner")

class PostsListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ("title", "attachment", "abstract", "date_pub")