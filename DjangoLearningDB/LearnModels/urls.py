from django.urls import path
from .views import PostList, DetailPost, SearchPost, NewsCreate, NewsEdit, NewsDelete

urlpatterns = [
    path('', PostList.as_view(), name='post_list'),
    path('<int:pk>', DetailPost.as_view(), name='post_detail'),
    path('search/', SearchPost.as_view(), name='post_search'),
    path('news/create/', NewsCreate.as_view(), name='news_create'),
    path('news/<int:pk>/edit/', NewsEdit.as_view(), name='news_edit'),
    path('news/<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
    path('articles/create/', NewsCreate.as_view(), name='articles_create'),
    path('articles/<int:pk>/edit/', NewsEdit.as_view(), name='articles_edit'),
    path('articles/<int:pk>/delete/', NewsDelete.as_view(), name='articles_delete'),
]