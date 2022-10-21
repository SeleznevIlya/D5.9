import django_filters
from django_filters import FilterSet
from .models import Post


class PostFilter(FilterSet):
    # author__id_user_id__username = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Post

        fields ={
            'author__id_user_id__username': ['icontains'],
            'header': '',
            'date_time': ['gt']
        }
        # fields = [
        #     'author__id_user_id__username',
        #     'header',
        #     #'date_time'
        # ]