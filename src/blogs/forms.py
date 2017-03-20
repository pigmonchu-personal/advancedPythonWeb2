from django import forms
from django.contrib.admin import widgets

from blogs.models import Post

class PostForm(forms.ModelForm):

    blog_id = forms.CharField(
        widget=forms.Select,
        label='Blog'
    )

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Post
        fields = ("title", "abstract", "body", "attachment", "date_pub", "categories")
        widgets = {
            'date_pub': forms.SelectDateWidget(
                empty_label=("Año", "Mes", "Día"),
                attrs={'class': 'date'}
            )
        }


