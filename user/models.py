import uuid
from django.db import models
from django.contrib.auth.models import User
from explore.models import Subject, Topic
from config import ProcessingStatus

class UserSubject(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    status = models.CharField(max_length=32, default=ProcessingStatus.PROCESSING)
    tracking_id = models.UUIDField(unique=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.tracking_id is None:
            self.tracking_id = uuid.uuid4()
        super().save(*args, **kwargs)
    class Meta:
        unique_together = ['user', 'subject']

class UserTopic(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    confidence_level = models.IntegerField()
    course_find_status = models.CharField(max_length=32, null=True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'topic']
        