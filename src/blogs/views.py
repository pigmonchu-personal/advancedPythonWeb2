from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View

from blogs.forms import PostForm
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


class NewPostView(View):

    @method_decorator(login_required)
    def get(self, request):
        form = PostForm(user=request.user)
        context = {
            "form": form
        }
        return render(request, 'blogs/new_post.html', context)


    @method_decorator(login_required)
    def post(self, request):
        form = PostForm(request.POST, user=request.user)
        message = ""

        if form.is_valid():
            form.instance.blog_id = form.data.get("blog_id")
            post = form.save()

            form = PostForm(user=request.user)
            message = "Se ha creado correctamente el post"

        context = {
            "form": form,
            "message": message
        }
        return render(request, 'blogs/new_post.html', context)


