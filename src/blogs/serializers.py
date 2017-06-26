from django.urls import reverse
from django.utils import timezone
from rest_framework import serializers

from blogs.models import Blog, Post


class BlogSerializer(serializers.ModelSerializer):

    posts = serializers.StringRelatedField(many=True)
    url = serializers.SerializerMethodField()

    class Meta:
        model = Blog
        fields = ("id", "name", "description", "owner", "url", "posts")

    def get_url(self, obj):
        request = self.context.get("request")
        return request.get_host() + reverse('blog_detail', args=[obj.id])

class PostsListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ("id", "title", "attachment", "abstract", "date_pub")


class PostsRetrieveSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ("title", "abstract", "body", "categories", "attachment", "attachment_description", "blog", "date_pub")


class MediaSerializer(serializers.ModelSerializer):

    class Meta:

        model = Post
        fields = ("attachment",)
        extra_kwargs = {'attachment': {'write_only': True}}

    def validate_attachment(self, value):

        return value is not None


class PostSerializer(serializers.ModelSerializer):

    class Meta:

        model = Post
        fields = ("id", "title", "abstract", "body", "categories", "attachment", "attachment_description", "blog", "date_pub")

    def validate_blog(self, value):
        user = self.context.get("request").user
        view = self.context.get("view")

#       El blog debe pertenecer al usuario que hace la modificación
#       No se debe validar en el caso de un superusuario haciendo un update (por si quiere hacer no público el post de otro usuario)
        if self.context.get("request").user.id == value.owner.id or (view.action == "update" and user.is_superuser):
            return value

        raise serializers.ValidationError(_("El blog informado no pertenece al usuario"))
