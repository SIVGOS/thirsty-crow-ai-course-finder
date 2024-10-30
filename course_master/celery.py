import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'course_master.settings')
app = Celery('course_master_celery')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()