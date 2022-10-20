from django_filters import FilterSet
from .models import Post


class PostFilter(FilterSet):

    class Meta:
        model = Post

        fields ={
            'author__id_user_id__username': ['icontains'],
            'header': '',
            'date_time': ['gt']
        }