# -*- coding: utf-8 -*-
# TODO: Write here your API ViewSets
from rest_framework.generics import CreateAPIView

from microservice.models import File
from microservice.serializers import FileSerializer


class FileUploadApiView(CreateAPIView):
    queryset = File.objects.all()
    serializer_class = FileSerializer