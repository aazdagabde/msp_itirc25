import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'station_climatique.settings')

app = Celery('station_climatique')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
