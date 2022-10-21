from django.urls import path
from .views import PostList, DetailPost, SearchPost, search_post

urlpatterns = [
    path('', PostList.as_view(), name='post_list'),
    path('<int:pk>', DetailPost.as_view(), name='post_detail'),
    path('search/', SearchPost.as_view(), name='post_search')
]