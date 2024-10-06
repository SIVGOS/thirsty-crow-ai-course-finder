from celery import shared_task
from user.models import UserSubject, UserTopic
from .models import Topic
from .helpers import get_videos_for_topic
from constants import ProcessingStatus

@shared_task
def populate_videos(user_subject_id):
    user_subject = UserSubject.objects.get(id=user_subject_id)
    user_topics = UserTopic.objects.filter(user=user_subject.user, topic__subject=user_subject.subject)
    for user_topic in user_topics:
        get_videos_for_topic(user_topic)
    user_subject.status = ProcessingStatus.PROCESSED
    user_subject.save()
