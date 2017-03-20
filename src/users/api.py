from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from users.permissions import UserPermission
from users.serializers import UserSerializer


class UserViewSet(GenericViewSet):

    permission_classes = (UserPermission,)

    def create(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def retrieve(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        self.check_object_permissions(request, user)
        serializer = UserSerializer(user)
        return Response(serializer.data)


    def update(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        self.check_object_permissions(request, user)

        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Ya que no se especifica en la petición y me gusta la posibilidad de cambiar sólo ciertas partes del usuario he creado este método
    def partial_update(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        self.check_object_permissions(request, user)

        serializer = UserSerializer(user, data=request.data)
        serializer.fields["email"] = serializers.EmailField(required=False)
        serializer.fields["password"] = serializers.CharField(required=False)
        serializer.fields["username"] = serializers.CharField(required=False)
        serializer.fields["first_name"] = serializers.CharField(allow_blank=True, required=False)
        serializer.fields["last_name"] = serializers.CharField(allow_blank=True, required=False)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def destroy(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        self.check_object_permissions(request, user)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)