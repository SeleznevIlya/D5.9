from .models import Post
from django import forms


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = [
            'author__id_user_id__username',
            'header',
            #'date_time',
        ]