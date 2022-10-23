from django.forms import DateInput
from django_filters import FilterSet, DateFilter
from .models import Post


class PostFilter(FilterSet):
    # author__id_user_id__username = django_filters.CharFilter(lookup_expr='icontains')
    """Date_time выводит виджет календаря при выборе даты за счёт атрибуты widget"""
    date_time = DateFilter(lookup_expr='gt', widget=DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Post

        fields ={
            'author__id_user_id__username': ['icontains'],
            'header': ['icontains'],

        }
