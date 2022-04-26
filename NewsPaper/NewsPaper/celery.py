import os
from celery.schedules import crontab
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPaper.settings')

app = Celery('NewsPaper')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.broker_url = 'reddis://localhost:6379/0'

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send_mail_every_monday_8am': {
        'task': 'news.tasks.send_mail_for_sub_every_week',
        'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
    },
}
