from .models import Post
from django import forms
from django.core.exceptions import ValidationError


class PostForm(forms.ModelForm):
    author__id_user_id__username = forms.CharField()
    #date_time = forms.DateTimeField()
    class Meta:
        model = Post
        fields = [
            #'author__id_user_id__username',
            'header',
            #'date_time',
        ]

    # def clean(self):
    #     cleaned_data = super().clean()
    #     user = "author__id_user_id__username"
    #     username = cleaned_data.get(user)
    #     if username is None:
    #         raise ValidationError({
    #             "author__id_user_id__username": "Имя пользователя не может быть пустым."
    #         })
    #
    #     return cleaned_data