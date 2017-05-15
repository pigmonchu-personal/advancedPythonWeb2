from rest_framework.mixins import CreateModelMixin
from rest_framework.viewsets import GenericViewSet

from microservice.models import File
from microservice.serializers import FileSerializer


class FileUploadViewSet(CreateModelMixin, GenericViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer



