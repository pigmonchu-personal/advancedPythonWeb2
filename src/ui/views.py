from django.shortcuts import redirect
from django.utils import translation
from django.views import View

from django.utils.translation import ugettext as _

class TranslateView(View):

    def translate(self, form):
        fields = form.fields.keys()

        for field in fields:
            form.fields.get(field).label = _(form.fields.get(field).label)


class ChangeLanguage(View):

    def get(self, request, language):
        """
        Modificamos el LANGUAGE_SESSION_KEY para mantener el idioma seleccionado en toda la sesión
        """
        request.session[translation.LANGUAGE_SESSION_KEY] = language
        return redirect(request.META.get("HTTP_REFERER", "posts_list"))
