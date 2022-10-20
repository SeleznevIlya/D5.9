from django.urls import path
from .views import PostList, DetailPost, SearchPost

urlpatterns = [
    path('', PostList.as_view()),
    path('<int:pk>', DetailPost.as_view()),
    path('search', SearchPost.as_view())
]