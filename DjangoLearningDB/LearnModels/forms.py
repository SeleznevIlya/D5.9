from .models import Post
from django import forms
from django.core.exceptions import ValidationError


class PostForm(forms.ModelForm):
    text = forms.CharField(min_length=50, )
    header = forms.CharField(min_length=5)
    class Meta:
        model = Post
        fields = ['category', 'header', 'text', 'author'
            #'date_time',
        ]

    def clean(self):
        cleaned_data = super().clean()
        category = cleaned_data.get('category')
        if category is None:
            raise ValidationError({
                "category": "Категория не может быть пустой"
            })
        header = cleaned_data.get('header')
        if header is None:
            raise ValidationError({
                "header": "Error: пустой заголовок"
            })
        text = cleaned_data.get('text')
        if text is None:
            raise ValidationError({
                "header": "Error: пустой текст"
            })
        return cleaned_data