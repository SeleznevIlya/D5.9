from django.shortcuts import render
from .models import Post
from django.views.generic import ListView, DetailView


class PostList(ListView):
    model = Post
    ordering = '-date_time'

    template_name = 'posts.html'

    context_object_name = 'posts'


class DetailPost(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'
