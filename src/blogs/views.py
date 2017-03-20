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
        form = PostForm()
        #El siguiente método debería estar en el __init__ de PostForm, pero no sé como hacerlo. Pendiente de investigar
        self.__load_blog_user(form, request.user)
        context = {
            "form": form
        }
        return render(request, 'blogs/new_post.html', context)


    @method_decorator(login_required)
    def post(self, request):
        form = PostForm(request.POST)
        self.__load_blog_user(form, request.user)
        message = ""

        if form.is_valid():
            form.instance.blog_id = form.data.get("blog_id")
            post = form.save()

            form = PostForm()
            self.__load_blog_user(form, request.user)
            message = "Se ha creado correctamente el post"

        context = {
            "form": form,
            "message": message
        }
        return render(request, 'blogs/new_post.html', context)

    def __load_blog_user(self, form, user):
        blogs = Blog.objects.filter(owner=user.id)
        dBlog = [('', '------')]
        for blog in blogs:
            t = (blog.id, blog.__str__())
            dBlog.append(t)

        tBlog = tuple(dBlog)

        form.fields["blog_id"].widget.choices = tBlog
        return

        tBlog = tuple(dBlog)

