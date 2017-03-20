from django.contrib import admin

from blogs.models import Category, Blog, Post, Profile

admin.site.register(Category)
admin.site.register(Blog)
admin.site.register(Post)
admin.site.register(Profile)
