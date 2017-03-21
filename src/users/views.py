from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.contrib.auth.models import User
from django.db import Error, IntegrityError
from django.shortcuts import render, redirect
from django.views import View

from blogs.models import Blog
from users.forms import LoginForm, SignupForm


class LoginView(View):

    def get(self, request):
        context = {
            'form': LoginForm()
        }
        return render(request, 'login.html', context)

    def post(self, request):
        form = LoginForm(request.POST)
        context = dict()
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                request.session["default-language"] = "es"
                django_login(request, user)
                url = request.GET.get('next', '/')
                return redirect(url)
            else:
                form.add_error("__all__", "Wrong username or password")

        context["form"] = form
        return render(request, 'login.html', context)


class SignupView(View):

    def get(self, request):
        context = {
            'form': SignupForm()
        }

        return render(request, 'signup.html', context)

    def post(self, request):
        form = SignupForm(request.POST)
        context = dict()
        if form.is_valid():
            if User.objects.filter(username=form.cleaned_data.get("username")).exists():
                form.add_error("username", "Username already exists")
            else:
                user = User()

                user.username = form.cleaned_data.get("username")
                user.set_password(form.cleaned_data.get("password"))
                user.first_name = form.cleaned_data.get("first_name")
                user.last_name = form.cleaned_data.get("last_name")
                user.email = form.cleaned_data.get("email")

                try:
                    user.save()

                    blog = Blog()
                    if user.first_name or user.last_name:
                        blog.name = "Blog de " + user.first_name + " " + user.last_name
                    else:
                        blog.name = "Blog de " + user.username

                    blog.owner = user

                    blog.save()

                    url = request.GET.get('next', '/new-post')
                    return redirect(url)

                except Error as err:
                    form.add_error("__all__", "Error en acceso a base de datos")
                    print("Error en acceso a base de datos: ", err)

        context["form"] = form
        return render(request, 'signup.html', context)


def logout(request):
    django_logout(request)
    return redirect('login')

