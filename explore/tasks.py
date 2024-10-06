from celery import shared_task
from user.models import UserSubject, UserTopic
from .models import Topic

@shared_task
def populate_tests(user_subject_id):
    topics = UserTopic.objects.filter()