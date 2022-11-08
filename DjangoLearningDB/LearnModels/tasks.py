import os
from dotenv import load_dotenv
from django.shortcuts import redirect, render, reverse
from .models import Post, User, Category, Subscribers
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from datetime import datetime, date, timedelta

load_dotenv()


def send_message(pk_, id_categories_):
    post = Post.objects.get(id=pk_)
    emails = User.objects.filter(category__in=id_categories_).values('email').distinct()
    email_list = [item['email'] for item in emails]
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
        to=email_list,
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def week_news():
    start = datetime.now() - timedelta(7)
    finish = datetime.now()
    categories = Category.objects.all()

    for category_ in categories:
        post_list = Post.objects.filter(date_time__range = (start, finish), category=category_.pk)
        print(post_list)
        email_list = []
        #print(category_)
        for user_ in User.objects.all():
            user_email = Subscribers.objects.filter(category=category_.pk, user=user_.pk)
            if user_email and user_email not in email_list:
            #if user_email:
                email_list.append(user_.email)
        print(email_list)

        if post_list:
            html_content = render_to_string(
                'week_news.html',
                {
                    'posts': post_list,
                    'category': category_.category_name
                }
            )
            msg = EmailMultiAlternatives(
                subject="Новости за неделю",
                from_email=os.getenv('EMAIL_GOOGLE_FULL'),
                to=email_list,
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()








