import os
from celery import Celery

# set default django settings module for the 'celery' program
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mainashop.settings')

app = Celery('mainashop.settings')
app.config_from_object('django.conf:settings', namespace = 'CELERY')
app.autodiscover_tasks()