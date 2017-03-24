import datetime

from django.db.models import Q
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.viewsets import ReadOnlyModelViewSet, GenericViewSet, ModelViewSet

from blogs.models import Blog, Post, get_type_attachment
from blogs.permissions import PostPermission
from blogs.serializers import PostsListSerializer, PostSerializer, BlogSerializer


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
        return PostsListSerializer if self.action == "list" else PostSerializer

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
        self.save_with_attachment_type(serializer)

    def perform_update(self, serializer):
        self.save_with_attachment_type(serializer)

    def save_with_attachment_type(self, serializer):
        if serializer.validated_data.get("attachment"):
            serializer.validated_data["attachment_type"] = get_type_attachment(serializer.validated_data.get("attachment"))

        serializer.save()



