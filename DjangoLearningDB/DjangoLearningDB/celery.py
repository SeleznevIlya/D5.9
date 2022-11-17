import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoLearningDB.settings')

app = Celery('DjangoLearningDB')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'action_every_monday_8am':{
        'task': 'LearnModels.tasks.week_news',
        'schedule': crontab(hour=6, minute=0, day_of_week='thursday'),
        'args': (),
    }
}

