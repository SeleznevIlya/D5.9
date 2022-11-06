import os
from dotenv import load_dotenv
from django.shortcuts import redirect, render, reverse
from .models import Post, User, Category, Subscribers
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

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
        from_email=os.getenv('EMAIL_YANDEX_FULL'),
        to=email_list,
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()








