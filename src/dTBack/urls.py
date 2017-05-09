"""dTBack URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework.routers import DefaultRouter

from blogs.api0 import BlogsAPI
from blogs.api import BlogViewSet, PostViewSet
from blogs.views import blogs_list, posts_list, posts_username_list, post_complete, NewPostView, NewBlogView, \
    blog_detail
from ui.views import ChangeLanguage
from users.api import UserViewSet
from users.views import LoginView, SignupView, logout

router = DefaultRouter()
router.register("users", UserViewSet, base_name="users_api")
router.register("blogs", BlogViewSet, base_name="blogs_api")
router.register("posts", PostViewSet, base_name="posts_api")

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^change-language/(?P<language>.+)$', ChangeLanguage.as_view(), name="change-language"),

#web en backend
    url(r'^$', posts_list, name="posts_list"),
    url(r'^blogs/?$', blogs_list, name="blogs_list"),
    url(r'^blog/(?P<blog_id>[0-9]+)/?$', blog_detail, name="blog_detail"),
    url(r'^blogs/(?P<username>[\w.%+-]+)/?$', posts_username_list, name="posts_username_list"),
    url(r'^blogs/(?P<username>[\w.%+-]+)/(?P<post_id>[0-9]+)/?$', post_complete, name="post_complete"),
    url(r'^new-post/?$', NewPostView.as_view(), name="new_post"),
    url(r'^new-blog/?$', NewBlogView.as_view(), name="new_blog"),

    #Acceso al sistema
    url(r'^login/?$', LoginView.as_view(), name="login"),
    url(r'^signup/?$', SignupView.as_view(), name="signup"),
    url(r'^logout/?$', logout, name="logout"),

#API
    url(r'^api/0.1/blogs/$', BlogsAPI.as_view(), name="blogs_api"),
# API Routers
    url(r'^api/1.0/', include(router.urls)),

]

