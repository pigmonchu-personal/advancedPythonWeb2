# -*- coding: utf-8 -*-
from django.db import models

from microservice.validators import validate_file_type


class File(models.Model):

    file = models.FileField(upload_to='media', validators=[validate_file_type])

