# -*- coding: utf-8 -*-
from django.db import models

from microservice import settings



class File(models.Model):
    file = models.FileField(upload_to='uploads')
#    owner = settings.REST_FRAMEWORK.get("UNAUTHENTICATED_USER")