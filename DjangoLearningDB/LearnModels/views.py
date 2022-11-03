from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render, reverse, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views import View
from .filters import PostFilter
from .forms import PostForm
from .models import Post, Subscribers
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail


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

            return super().form_valid(form)


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


class SubscribersView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'subscribe_created.html', {})

    def post(self, request, *args, **kwargs):
        subscribe = Subscribers(
            user=request.POST['user'],
            category=request.POST['category'],
        )
        subscribe.save()



        send_mail(
            subject=f"{Post.objects.get('header')}",
            message=f"{Post.objects.get('text')[:50]}"
        )
        return redirect('/posts/')