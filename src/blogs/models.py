import datetime
import urllib

from django.contrib.auth.models import User
from django.db import models

from django.utils.translation import ugettext as _

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

    blog = models.ForeignKey(Blog, related_name="posts")

    created_at = models.DateTimeField(auto_now_add=True)  # automáticamente añada la fecha de creación
    modified_at = models.DateTimeField(auto_now=True)  # automáticamente actualiza la fecha al guardar

    def __str__(self):
        return self.blog.name + ": " + self.blog.owner.username + " - " + self.title


def get_type_attachment(url):
    try:
        response = urllib.request.urlopen(url)
    except:
        return Post.NONE

    if response.getcode() != 200:
        return Post.NONE

    content_type = [header for header in response.info()._headers if header[0] == 'Content-Type']
    if content_type and 'image' in content_type[0][1]:
        return Post.IMAGE

    if content_type and 'video' in content_type[0][1]:
        return Post.VIDEO

    return Post.NONE