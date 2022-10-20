from django_filters import FilterSet
from .models import Post


class PostFilter(FilterSet):

    class Meta:
        model = Post

        fields ={
            'author': ['self.id_user.username__icontains'],
            'header': '',
            'date_time': ['gt']
        }