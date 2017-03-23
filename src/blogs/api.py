import datetime

from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.viewsets import ReadOnlyModelViewSet, GenericViewSet, ModelViewSet

from blogs.models import Blog, Post
from blogs.permissions import PostPermission
from blogs.serializers import BlogsListSerializer, PostsListSerializer, PostSerializer


class BlogViewSet(ReadOnlyModelViewSet):

    queryset = Blog.objects.select_related("owner").all()
    permission_classes = (PostPermission,)
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ("owner__username",)
    ordering_fields = ("name", "id", "description", "owner")
    serializer_class = BlogsListSerializer

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
            # if not user.is_superuser or self.action == 'update':
            # Me parece mucho riesgo que un administrador pueda modificar el contenido de mi blog (yo lo prohibiría o al menos no dejaría modificar ni título, ni abstract, ni body. Dejaría que modificara la fecha de publicación a infinito
            if not user.is_superuser:
                queryset = queryset.filter(blog__owner=user)
        return queryset

    def perform_create(self, serializer):

#        serializer.validated_data["date_pub"] = datetime.datetime.now()

        serializer.save()






