import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.datetime_safe import strftime
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _

from blogs.forms import PostForm, BlogForm
from blogs.models import Blog, Post, get_type_attachment_by_file
from dTBack import settings
from dTBack.celery import resizeImage
from ui.views import TranslateView


def blogs_list(request):
    blogs = Blog.objects.select_related("owner").all()

    context = {
        'blogs': blogs
    }

    return render(request, 'blogs/list.html', context)


def blog_detail(request, blog_id):
    posts = Post.objects.select_related("blog", "blog__owner",).filter(blog__id=blog_id).order_by("-date_pub")

    if len(posts) != 0:
        blog = posts[0].blog
    else:
        blog = Blog.objects.select_related("owner").get(pk=blog_id)

    username = blog.owner.username
    if username != request.user.username and not request.user.is_superuser:
        posts = posts.filter(date_pub__lte=datetime.datetime.now())

    context = {
        'posts': posts,
        'blog': blog
    }

    return render(request, 'blogs/posts_blog.html', context)

def posts_list(request):

    posts = Post.objects.select_related("blog", "blog__owner","blog__owner__profile",).filter(date_pub__lte=datetime.datetime.now()).order_by("-date_pub")

    context = {
        'posts': posts,
        'responsiveness': settings.WEB_RESPONSIVE,
    }

    return render(request, 'blogs/posts_list.html', context)

def posts_username_list(request, username):

    posts = Post.objects.select_related("blog", "blog__owner", "blog__owner__profile",).filter(blog__owner__username=username).order_by("-date_pub")

    if username != request.user.username and not request.user.is_superuser:
        posts = posts.filter(date_pub__lte=datetime.datetime.now())

    context = {
        'posts': posts
    }

    return render(request, 'blogs/posts_username_list.html', context)

def post_complete(request, username, post_id):

    try:
        post = Post.objects.select_related("blog", "blog__owner", "blog__owner__profile").prefetch_related("categories").get(id=post_id)

        format = "%Y%m%d%H%M%S"
        if post.blog.owner.username != username or (username != request.user.username and not request.user.is_superuser and strftime(post.date_pub, format) >= strftime(datetime.datetime.now(), format)):
            return render(request, '404.html', {}, status=404)
        else:
            context = {
                'post': post,
                'categories': post.categories.all(),
                'media_path' : settings.MEDIA_URL
            }

            return render(request, 'blogs/post.html', context)

    except Post.DoesNotExist as err:
        return render(request, '404.html', {}, status=404)


class NewPostView(TranslateView):

    @method_decorator(login_required)
    def get(self, request):
        form = PostForm(user=request.user)
        self.translate(form)
        context = {
            "form": form
        }
        return render(request, 'blogs/new_post.html', context)


    @method_decorator(login_required)
    def post(self, request):

        form = PostForm(request.POST, request.FILES, user=request.user)
        self.translate(form)
        message = ""

        if form.is_valid():
            form.instance.blog_id = form.data.get("blog_id")
            if not form.instance.date_pub:
                form.instance.date_pub = datetime.datetime.now()

            there_Is_A_File = False

            if form.instance.attachment:
                there_Is_A_File = True
                form.instance.attachment_type = form.instance.get_attachment_type()
                if form.instance.attachment_type == Post.NONE:
                    form.instance.attachment = None
                
            form.save()
            if there_Is_A_File and form.instance.attachment_type == Post.IMAGE:
                resizeImage.delay(form.instance.attachment.name, 400)

            form = PostForm(user=request.user)

            if there_Is_A_File and form.instance.attachment_type == Post.NONE:
                message = _("Se ha creado correctamente el post sin media file. Ver tipos de fichero admitidos.")
            else:
                message = _("Se ha creado correctamente el post")

        context = {
            "form": form,
            "message": message
        }
        return render(request, 'blogs/new_post.html', context)


class NewBlogView(TranslateView):

    @method_decorator(login_required)
    def get(self, request):
        form = BlogForm()
        self.translate(form)
        context = {
            "form": form
        }
        return render(request, 'blogs/new_blog.html', context)


    @method_decorator(login_required)
    def post(self, request):
        blog_with_user = Blog(owner=request.user)
        form = BlogForm(request.POST, instance=blog_with_user)
        self.translate(form)
        message = ""

        if form.is_valid():
            form.save()

            form = BlogForm()
            message = _("Se ha creado correctamente el blog")

        context = {
            "form": form,
            "message": message
        }
        return render(request, 'blogs/new_blog.html', context)

