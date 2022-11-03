from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.urls import reverse
from django.conf import settings


class Author(models.Model):
    id_user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        sum_posts_rating = self.post_set.all().aggregate(Sum('post_rating'))['post_rating__sum']*3
        sum_comments = self.id_user.comment_set.all().aggregate(Sum('comment_rating'))['comment_rating__sum']
        sum_comments_post = self.post_set.all().aggregate(Sum('comment__comment_rating'))['comment__comment_rating__sum']
        #result_rating
        self.rating = sum_posts_rating + sum_comments + sum_comments_post
        self.save()

    def __str__(self):
        return f'{self.id_user.username}'


class Category(models.Model):
    category_name = models.CharField(max_length=255, unique=True)
    subscribers = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Subscribers')

    def __str__(self):
        return f'{self.category_name}'


class Subscribers(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Post(models.Model):

    TYPE = [
        ('news', 'Новости'),
        ('article', 'Статья'),
    ]

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    type_of_post = models.CharField(max_length=10,
                                    choices=TYPE,
                                    default='news')
    date_time = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    header = models.CharField(max_length=255)
    text = models.TextField(default='Здесь должен быть текст статьи/новости')
    post_rating = models.IntegerField(default=0)

    def like(self):
        self.post_rating += 1
        self.save()

    def dislike(self):
        self.post_rating -= 1
        self.save()

    def preview(self):
        return f'{self.text[:124]}...'

    def __str__(self):
        return f'{self.header.title()}'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField()
    date_time = models.DateTimeField(auto_now_add=True)
    comment_rating = models.IntegerField(default=0)

    def like(self):
        self.comment_rating += 1
        self.save()

    def dislike(self):
        self.comment_rating -= 1
        self.save()

    def __str__(self):
        return f'{self.user}: {self.comment_text[:20]}'



