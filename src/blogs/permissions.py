from rest_framework.permissions import BasePermission

from blogs.models import Category, Post



class PostPermission(BasePermission):

    def has_permission(self, request, view):
        if view.action in {'list', 'retrieve'}:
            return True

        return request.user.is_authenticated


    def has_object_permission(self, request, view, obj):
        if view.action == 'retrieve':
            return True

        if not request.user.is_authenticated:
            return False

        if view.action == 'update' and request.user.is_superuser:
            # sólo puede modificar la fecha de publicación
            input_entity = request.data
            db_entity = obj

            if input_entity.get("title") != db_entity.title or \
               input_entity.get("abstract") != db_entity.abstract or \
               input_entity.get("body") != db_entity.body or \
               input_entity.get("blog") != db_entity.blog.id:

                return False

            db_categories = db_entity.categories.all()
            db_categories_id = []
            for category in db_categories:
                db_categories_id.append(category.id)

            if sorted(db_categories_id) != sorted(input_entity.get("categories")):
                return False

        return request.user.is_authenticated