from rest_framework.permissions import BasePermission


class UserPermission(BasePermission):

    def has_permission(self, request, view):

        # cualquiera autenticado puede acceder al detalle para ver, actualizar o borrar
        if request.user.is_authenticated() and view.action in ("retrieve", "update", "destroy", "partial_update"):
            return True

        # si es superusuario y quiere acceder al listado
        if request.user.is_superuser and view.action == "list":
            return True

        # cualquiera puede crear un usuario (POST)
        if view.action == "create":
            return True

        return False

    def has_object_permission(self, request, view, obj):
        # si es admin o si es él mismo, le dejamos
        return request.user.is_superuser or request.user == obj
