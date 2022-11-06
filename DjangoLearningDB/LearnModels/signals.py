from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives, mail_managers
from django.template.loader import render_to_string
from .models import Post, Category, User


@receiver(post_save, sender=Post)
def notify_post(sender, instance, created, **kwargs):
    if created:
        subject = f'Добавлена новость:{instance.header} от {instance.date.strftime( "%d %m %Y" )}'
    else:
        subject = f'Изменена новость:{instance.header} от {instance.date.strftime( "%d %m %Y" )}'

    try:
        mail_managers(
            subject=subject,
            message=f'{instance.header} http://127.0.0.1/posts/{instance.id}'
        )
    except Exception:
        print('ошибка отправки сообщения')



