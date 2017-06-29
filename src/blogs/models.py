import datetime
import os

import magic
from celery import shared_task
from django.contrib.auth.models import User
from django.core.files import File
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models

from dTBack import settings
from PIL import Image
from celery import shared_task
from resizeimage import resizeimage


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
            name, extension = os.path.splitext(self.attachment.file.name)

            if extension in settings.UPLOAD_FILE_EXTENSIONS.get("images"):
                return Post.IMAGE
            elif extension in settings.UPLOAD_FILE_EXTENSIONS.get("videos"):
                return Post.VIDEO
            else:
                return Post.NONE

        elif isinstance(self.attachment, File):
            content_type = magic.from_file(self.attachment.file.name, mime=True)

            try:
                if content_type in settings.UPLOAD_FILE_TYPES.get("images"):
                    return Post.IMAGE
                elif content_type in settings.UPLOAD_FILE_TYPES.get("videos"):
                    return Post.VIDEO
                else:
                    return Post.NONE
            except:
                return Post.NONE
        else:
            return Post.NONE

    @shared_task
    def resizeImage(id):

        post = Post.objects.get(pk=id)

        if post.attachment_type != post.IMAGE:
            return

        source = post.attachment.name

        print('Resizing {0}'.format(source))
        fromImage = os.path.join(settings.MEDIA_ROOT, source)
        toPath = os.path.join(settings.STATIC_ROOT, 'images', 'posts')

        filename, file_extension = os.path.splitext(source)

        if not os.path.exists(fromImage) or not os.path.exists(toPath):
            return

        theImage = Image.open(fromImage)
        for width_image in settings.WEB_RESPONSIVE.get("dimensions"):
            newImage = resizeimage.resize_width(theImage, width_image)
            newFilename = filename + ("-%d" % width_image) + file_extension
            newImage.save(os.path.join(toPath, newFilename))
            print('new file: {0}'.format(newFilename))

