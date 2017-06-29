import datetime
import os

import magic
from django.contrib.auth.models import User
from django.core.files import File
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models

from dTBack import settings


class FILE(File):
    pass


class Profile(models.Model):
    user = models.OneToOneField(User)
    photo = models.URLField(null=True, blank=True)

class Category(models.Model):
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=255, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)  # automáticamente añada la fecha de creación
    modified_at = models.DateTimeField(auto_now=True)  # automáticamente actualiza la fecha al guardar

    def __str__(self):
        return self.name

class Blog(models.Model):
    name = models.CharField( max_length=150)
    description = models.CharField( max_length=400, blank=True, null=True)
    owner = models.ForeignKey(User)

    created_at = models.DateTimeField(auto_now_add=True)  # automáticamente añada la fecha de creación
    modified_at = models.DateTimeField(auto_now=True)  # automáticamente actualiza la fecha al guardar

    def __str__(self):
        return self.name + "(" + self.owner.first_name + " " + self.owner.last_name +")"

class Post(models.Model):

    VIDEO = "V"
    IMAGE = "I"
    NONE = "N"
    ATTACHMENT_TYPES = (
        (VIDEO, "Video"),
        (IMAGE, "Image"),
        (NONE, "None")
    )


    title = models.CharField(max_length=150)
    abstract = models.CharField(max_length=4000)
    body = models.TextField()
    categories = models.ManyToManyField(Category, null=True, default=None)
    date_pub = models.DateTimeField(default=datetime.datetime.now())
    attachment = models.FileField(null=True, blank=True)
    attachment_type = models.CharField(max_length=1, default=NONE, choices=ATTACHMENT_TYPES)
    attachment_description = models.CharField(max_length=255, null=True, blank=True)
    blog = models.ForeignKey(Blog, related_name="posts")

    created_at = models.DateTimeField(auto_now_add=True)  # automáticamente añada la fecha de creación
    modified_at = models.DateTimeField(auto_now=True)  # automáticamente actualiza la fecha al guardar


    def __str__(self):
        return self.blog.name + ": " + self.blog.owner.username + " - " + self.title

    def get_filename(self):
        filename, file_extension = os.path.splitext(self.attachment.name)
        return filename


    def get_filextension(self):
        filename, file_extension = os.path.splitext(self.attachment.name)
        return file_extension


    def get_attachment_type(self):

        if isinstance(self.attachment.file, InMemoryUploadedFile):
            content_type = self.attachment.file.content_type
        elif isinstance(self.attachment, File):
            content_type = magic.from_file(self.attachment.file.name, mime=True)
        else:
            return Post.NONE

        try:
            if content_type in settings.UPLOAD_FILE_TYPES.get("images"):
                return Post.IMAGE
            elif content_type in settings.UPLOAD_FILE_TYPES.get("videos"):
                return Post.VIDEO
            else:
                return Post.NONE
        except:
            return Post.NONE

def get_type_attachment_by_file(file):
    return get_type_attachment(file.content_type)


def get_type_attachment_by_name(file):
    return get_type_attachment(magic.from_file(file, mime=True))

def get_type_attachment(content_type):
    try:
        if content_type in settings.UPLOAD_FILE_TYPES.get("images"):
            return Post.IMAGE
        elif content_type in settings.UPLOAD_FILE_TYPES.get("videos"):
            return Post.VIDEO
        else:
            return Post.NONE
    except:
        return Post.NONE

