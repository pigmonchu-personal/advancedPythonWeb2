import datetime
import os

from django.db.models import Q
from django.utils.translation import ugettext as _
from rest_framework import mixins
from rest_framework import serializers
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.parsers import FileUploadParser
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet, GenericViewSet

from blogs.models import Blog, Post
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

    #Al final hago dos validaciones. Antes de subir por extensión. Si aún así me la quieren colar, se hace una validación por fichero una vez subido. Si no es lo que se espera, se borra.
    #El consumo de ancho de banda del cliente solo se da si intenta engañar o si sube el fichero correcto

        serializer.validate_attachment()

#TODO Crear un comando de python que valide en media si los ficheros están asociados a algún post. Si no es así, borrarlos en media y en static. Programarlo con un CRON cada x horas (en función del movimiento de la plataforma)


        obj = self.get_object()
        oldFile = obj.attachment
        obj.attachment = serializer.initial_data.get('file')

        obj.save()

        o = Post.objects.select_related("blog").filter(pk=obj.pk)[0]
        file_type = o.get_attachment_type()

        if file_type == o.NONE:
            os.remove(o.attachment.file.name)
            o.attachment = oldFile
            o.save()
            raise serializers.ValidationError(_("Fichero de tipo incorrecto"))

        o.attachment_type = file_type
        o.save()
        o.resizeImage.delay(o.id)











