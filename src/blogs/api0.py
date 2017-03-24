from enum import Enum

from django.contrib.auth.models import User
from django.core.exceptions import FieldError
from django.urls import reverse
from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from blogs.models import Blog
from blogs.serializers0 import BlogsListSerializer


class USERNAME(Enum):
    NON_EXIST = -1
    NOT_INFORMED = 0

class BlogsAPI(GenericAPIView):
    sort_fields = ['name', 'description', "owner", "id"]

    def get(self, request):

        user_id = self.__filter_username()
        if user_id == USERNAME.NOT_INFORMED:
            self.queryset = Blog.objects.select_related("owner").all()
        else:
            self.queryset = Blog.objects.select_related("owner").filter(owner=user_id)

        sort = self.request.query_params.get('ordering', None)
        if sort is not None:
            sort = self.__sort_criteria(sort)
            self.queryset = self.queryset.order_by(*sort)

        try:
            page = self.paginate_queryset(self.queryset)
            serializer = BlogsListSerializer(page, many=True)
            for data in serializer.data:
                data["url"] = request.get_host() + data.get("url")

            return self.get_paginated_response(serializer.data)
        except FieldError as err:
            error = dict()
            error['exception'] = 'Unknown Field'
            error['message'] = '%s' % err

            print(error)
            return Response(error, status=status.HTTP_400_BAD_REQUEST)

    def __sort_criteria(self, maybe_sort):
        maybe_sort = maybe_sort.split()
        sort = []
        for criterion in maybe_sort:
            if criterion in self.sort_fields or ('-' in criterion and criterion.index('-') == 0 and criterion[1:] in self.sort_fields):
                sort.append(criterion)
        return sort

    def __filter_username(self):
        username = self.request.query_params.get('owner', None)
        if username is not None:
            users = User.objects.filter(username=username)
            if users.count() == 1:
                return users[0].id
            else:
                return USERNAME.NON_EXIST.value
        else:
            return USERNAME.NOT_INFORMED

