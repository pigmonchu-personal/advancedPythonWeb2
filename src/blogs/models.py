from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(User)
    photo = models.CharField(max_length=255, null=True, blank=True)

class Category(models.Model):
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=255, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)  # automáticamente añada la fecha de creación
    modified_at = models.DateTimeField(auto_now=True)  # automáticamente actualiza la fecha al guardar

    def __str__(self):
        return self.name

class Blog(models.Model):
    name = models.CharField(max_length=150)
    description = models.CharField(max_length=400, blank=True, null=True)
    owner = models.ForeignKey(User)

    created_at = models.DateTimeField(auto_now_add=True)  # automáticamente añada la fecha de creación
    modified_at = models.DateTimeField(auto_now=True)  # automáticamente actualiza la fecha al guardar

    def __str__(self):
        return self.name + "(" + self.owner.first_name + " " + self.owner.last_name +")"


class Post(models.Model):
    title = models.CharField(max_length=150)
    abstract = models.CharField(max_length=4000)
    body = models.TextField()
    categories = models.ManyToManyField(Category, null=True, default=None)
    date_pub = models.DateTimeField(null=True, blank=True)
    attachment = models.CharField(max_length=255, null=True, blank=True)
    attachment_caption = models.CharField(max_length=255, blank=True, null=True)

    blog = models.ForeignKey(Blog)

    created_at = models.DateTimeField(auto_now_add=True)  # automáticamente añada la fecha de creación
    modified_at = models.DateTimeField(auto_now=True)  # automáticamente actualiza la fecha al guardar

    def __str__(self):
        return self.blog.name + ": " + self.blog.owner.username + " - " + self.title

