from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        sum_posts_rating = self.Post_set.all().aggregate(sum_rating=sum('rating')*3)['sum_rating']
        sum_comments = self.user.Comment_set.all().aggregate(sum_rating=sum('comment_rating'))['sum_rating']
        sum_comments_post = self.user.Post_set.Comment_set.all().aggregate(sum_rating=sum('comment_rating'))['sum_rating']
        result_rating = sum_posts_rating + sum_comments + sum_comments_post
        self.save()


class Category(models.Model):
    category_name = models.CharField(max_length=255, unique=True)


class Post(models.Model):
    news = 'NS'
    article = 'AR'
    TYPE = [
        (news, 'Новости'),
        (article, 'Статья'),
    ]

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    type_of_post = models.CharField(max_length=2,
                                    choices=TYPE,
                                    default=news)
    date_time = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    header = models.CharField(max_length=255)
    text = models.TextField(default='Здесь должен быть текст статьи/новости')
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return f'{self.text[:124]}...'


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
