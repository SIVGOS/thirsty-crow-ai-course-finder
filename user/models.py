from django.db import models
from django.contrib.auth.models import User
from explore.models import Subject, Topic

class UserSubject(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)

class UserTopic(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    confidence_level = models.IntegerField()
    created_on = models.DateTimeField(auto_now_add=True)

