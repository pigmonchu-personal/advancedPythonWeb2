from django.db import Error
from django.shortcuts import render
from rest_framework import status

from blogs.models import Blog, Post


def blogs_list(request):
    blogs = Blog.objects.select_related("owner").all()

    context = {
        'blogs': blogs
    }

    return render(request, 'blogs/list.html', context)

def posts_list(request):
    posts = Post.objects.select_related("blog", "blog__owner", "blog__owner__profile",).order_by("-date_pub")

    context = {
        'posts': posts
    }

    return render(request, 'blogs/posts_list.html', context)

def posts_username_list(request, username):

    posts = Post.objects.select_related("blog", "blog__owner", "blog__owner__profile",).filter(blog__owner__username=username).order_by("-date_pub")

    context = {
        'posts': posts
    }

    return render(request, 'blogs/posts_username_list.html', context)

def post_complete(request, username, post_id):

    try:
        post = Post.objects.select_related("blog", "blog__owner", "blog__owner__profile").prefetch_related("categories").get(id=post_id)

        if post.blog.owner.username != username:
            return render(request, '404.html', {}, status=404)
        else:
            context = {
                'post': post,
                'categories': post.categories.all()
            }

            return render(request, 'blogs/post.html', context)

    except Post.DoesNotExist as err:
        return render(request, '404.html', {}, status=404)



