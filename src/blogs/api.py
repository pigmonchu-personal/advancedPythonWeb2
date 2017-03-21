import datetime

from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet, GenericViewSet, ModelViewSet

from blogs.models import Blog, Post
from blogs.serializers import BlogsListSerializer, PostsListSerializer


class BlogViewSet(ReadOnlyModelViewSet):

    queryset = Blog.objects.select_related("owner").all()
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ("owner__username",)
    ordering_fields = ("name", "id", "description", "owner")
    serializer_class = BlogsListSerializer


class PostViewSet(ModelViewSet):
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ("title", "body", "abstract")
    ordering_fields = ("title", "date_pub")
    ordering = ("-date_pub")
    serializer_class = PostsListSerializer

    def get_queryset(self):
        queryset = Post.objects.select_related("blog").all()

        user = self.request.user

        if user.is_anonymous():
           queryset = queryset.filter(date_pub__lte=datetime.datetime.now())
        else:
            if not user.is_superuser:
                queryset = queryset.filter(blog__owner=user)
        return queryset





