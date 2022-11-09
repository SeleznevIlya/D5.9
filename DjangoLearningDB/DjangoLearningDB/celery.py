import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoLearningDB.settings')

app = Celery('DjangoLearningDB')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()