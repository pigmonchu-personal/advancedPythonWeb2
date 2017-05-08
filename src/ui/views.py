from django.views import View

from django.utils.translation import ugettext as _

class TranslateView(View):

    def translate(self, form):
        fields = form.fields.keys()

        for field in fields:
            form.fields.get(field).label = _(form.fields.get(field).label)

