# -*- coding: utf-8 -*-

from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

from microservice.models import File
from microservice.serializers import FileSerializer


class FileUploadApiView(CreateAPIView):
    queryset = File.objects.all()
    serializer_class = FileSerializer
