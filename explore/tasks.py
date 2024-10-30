from celery import shared_task
from user.models import UserSubject, UserTopic
from .models import Subject
from .helpers import get_sub_topics, get_videos_for_topic
from config import ProcessingStatus    

@shared_task
def populate_topics(subject_id):
    subject = Subject.objects.get(id=subject_id)
    get_sub_topics(subject)
    subject.topics_created = True
    subject.save()

@shared_task
def populate_videos(user_subject_id):
    user_subject = UserSubject.objects.get(id=user_subject_id)
    user_topics = UserTopic.objects.filter(user=user_subject.user, topic__subject=user_subject.subject)
    for user_topic in user_topics:
        get_videos_for_topic(user_topic)
    user_subject.status = ProcessingStatus.PROCESSED
    user_subject.save()

@shared_task
def create_file(filename):
    with open(filename, 'w') as fp:
        fp.write('test test')