import datetime
import os

from django.db.models import Q
from rest_framework import mixins
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.parsers import FileUploadParser
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet, GenericViewSet

from dTBack.celery import resizeImage

import dTBack
from blogs.models import Blog, Post, get_type_attachment_by_name
from blogs.permissions import PostPermission, MediaPermission
from blogs.serializers import PostsListSerializer, PostSerializer, BlogSerializer, PostsRetrieveSerializer, \
    MediaSerializer


class BlogViewSet(ReadOnlyModelViewSet):

    queryset = Blog.objects.select_related("owner").all()
    permission_classes = (PostPermission,)
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ("owner__username",)
    ordering_fields = ("name", "id", "description", "owner")
    serializer_class = BlogSerializer

class PostViewSet(ModelViewSet):

    serializer_class = PostSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ("title", "body", "abstract")
    ordering_fields = ("title", "date_pub")
    ordering = ("-date_pub")
    permission_classes = (PostPermission,)

    def get_serializer_class(self):

        if self.action == "list":
            return PostsListSerializer
        elif self.action == "retrieve":
            return PostsRetrieveSerializer
        else:
            return PostSerializer

    def get_queryset(self):
        self.serializer_class = PostsListSerializer

        if self.action != "update":
            queryset = Post.objects.select_related("blog").all()
        else:
            queryset = Post.objects.prefetch_related("categories").select_related("blog").all()

        user = self.request.user

        if user.is_anonymous():
           queryset = queryset.filter(date_pub__lte=datetime.datetime.now())
        else:
            if not user.is_superuser:
                queryset = queryset.filter(Q(date_pub__lte=datetime.datetime.now()) | Q(blog__owner=user))
        return queryset

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()


class MediaViewSet(GenericViewSet, mixins.UpdateModelMixin):
    parser_classes = (FileUploadParser, )
    serializer_class = MediaSerializer
    permission_classes = (MediaPermission,)
    queryset = Post.objects.select_related("blog")
    filter_backends = (SearchFilter, OrderingFilter)


    def perform_update(self, serializer):

        #TODO: control de http-status y mensajes. Devuelve un 200 en todo caso a no ser que se produzca un error 500.

        obj = self.get_object()
        oldFile = obj.attachment
        obj.attachment = serializer.initial_data.get('file')
        obj.save()

        o = Post.objects.select_related("blog").filter(pk=obj.pk)[0]
        file_type = o.get_attachment_type()

        if file_type == o.NONE:
            o.attachment = oldFile
            o.save()
            return

        o.attachment_type = file_type
        o.save()

        if file_type == o.IMAGE:

#TODO gestionar el resizing to responsiveness directamente también desde el modelo -> migrar la semilla de resize desde el celery a models.Post
            resizeImage(o.attachment.name, 400)










