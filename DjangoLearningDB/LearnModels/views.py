import os

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views import View
from .filters import PostFilter
from .forms import PostForm
from .models import Post, Subscribers, Category
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import Group, User
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, EmailMultiAlternatives


class PostList(LoginRequiredMixin, ListView):
    model = Post
    ordering = '-date_time'

    template_name = 'posts.html'

    context_object_name = 'posts'

    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()

        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        context['get_category'] = Category.objects.all()
        return context


class DetailPost(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


class SearchPost(ListView):
    model = Post
    template_name = 'post_search.html'
    context_object_name = 'post_search'

    def get_queryset(self):
        queryset = super().get_queryset()

        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class NewsCreate(PermissionRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'news_create.html'
    permission_required = ('LearnModels.add_post',)

    def form_valid(self, form):
        post = form.save(commit=False)
        if self.request.method == 'POST':
            if self.request.path == '/posts/news/create/':
                post.type_of_post = 'news'
            else:
                post.type_of_post = 'articles'
        post.save()
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        post = Post(
            header = request.POST['header'],
            text=request.POST['text'],
            author_id=request.POST['author'],
            #category=request.POST['category']
        )
        post.save()

        primary_key = post.pk
        post_ = Post.objects.get(pk=primary_key)
        subscribers_list = []
        for category in post_.category.all():
            for user in category.user.all():
                if user not in subscribers_list:
                    subscribers_list.append(user)

        html_content = render_to_string(
            'subscribe_created.html',
            {
                'subscribe': post
            }
        )

        msg = EmailMultiAlternatives(
            subject=f'{post.header}',
            body=post.text,
            from_email=os.getenv('EMAIL_GOOGLE_FULL'),
            #from_email='seleznev.ilya.a@gmail.com',
            to=['helfik123_1998@mail.ru', ],
        )

        msg.attach_alternative(html_content, "text/html")
        msg.send()
        return redirect('/posts/')


class NewsEdit(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'
    permission_required = ('LearnModels.change_post',)


class NewsDelete(DeleteView):
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('post_list')


@login_required
def upgrage_me(request):
    user = request.user
    author_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        author_group.user_set.add(user)
    return redirect('/posts/')

def subscribes(request, i):
    user = User.objects.get(username=request.user)
    if user:
        cat1 = Category.objects.get(pk=i)
        cat1.subscriber.add(user)
    return redirect('/posts/')
