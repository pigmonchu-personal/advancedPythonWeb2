# -*- coding: utf-8 -*-
from rest_framework import serializers

from microservice.models import File
from microservice.validators import validate_file_type


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = '__all__'

    def validate_file(self, value):
        validate_file_type(value)