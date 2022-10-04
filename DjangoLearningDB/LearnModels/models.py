from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


class Author(models.Model):
    id_user = models.OneToOneField(User,
                                on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        sum_posts_rating = self.post_set.all().aggregate(Sum('post_rating'))['post_rating__sum']*3
        sum_comments = self.user.comment_set.all().aggregate(Sum('comment_rating'))['comment_rating__sum']
        sum_comments_post = self.user.post_set.comment_set.all().aggregate(Sum('Comment__comment_rating'))['Comment__sum_rating__sum']
        result_rating = sum_posts_rating + sum_comments + sum_comments_post
        self.save()


class Category(models.Model):
    category_name = models.CharField(max_length=255, unique=True)


class Post(models.Model):

    TYPE = [
        ('news', 'Новости'),
        ('article', 'Статья'),
    ]

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    type_of_post = models.CharField(max_length=1,
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
