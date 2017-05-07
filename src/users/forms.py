from django import forms
from django.utils.translation import ugettext as _

class LoginForm(forms.Form):
    username = forms.CharField(label=_('Usuario'),
                               required=True)
    password = forms.CharField(label=_('Contraseña'),
                               required=True,
                               widget=forms.PasswordInput())

class SignupForm(forms.Form):
    username = forms.CharField(label=_('Usuario'),
                               required=True)
    email = forms.EmailField(label=_("Correo electrónico"),
                             required=True)
    password = forms.CharField(label=_('Contraseña'),
                               required=True,
                               widget=forms.PasswordInput())
    confirm_password = forms.CharField(label=_("Repita Contraseña"),
                                       required=True,
                                       widget=forms.PasswordInput())
    first_name = forms.CharField(label=_("Nombre"),
                                 required=False)
    last_name = forms.CharField(label=_("Apellidos"),
                                required=False)

    def clean(self):
        dic = self.cleaned_data
        pass1 = dic.get('password')
        pass2 = dic.get('confirm_password')

        if pass1 and pass1 != pass2:
            raise forms.ValidationError({'confirm_password':[_("Las contraseñas no coinciden"), ]})

        return dic
