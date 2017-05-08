from django import forms

class LoginForm(forms.Form):


    username = forms.CharField(label='Usuario',
                               localize=True,
                               required=True)
    password = forms.CharField(label='Contraseña',
                               required=True,
                               localize=False,
                               widget=forms.PasswordInput())


class SignupForm(forms.Form):
    username = forms.CharField(label='Usuario',
                               required=True)
    email = forms.EmailField(label="Correo electrónico",
                             required=True)
    password = forms.CharField(label='Contraseña',
                               required=True,
                               widget=forms.PasswordInput())
    confirm_password = forms.CharField(label="Repita Contraseña",
                                       required=True,
                                       widget=forms.PasswordInput())
    first_name = forms.CharField(label="Nombre",
                                 required=False)
    last_name = forms.CharField(label="Apellidos",
                                required=False)

    def clean(self):
        dic = self.cleaned_data
        pass1 = dic.get('password')
        pass2 = dic.get('confirm_password')

        if pass1 and pass1 != pass2:
            raise forms.ValidationError({'confirm_password':[_("Las contraseñas no coinciden"), ]})

        return dic
