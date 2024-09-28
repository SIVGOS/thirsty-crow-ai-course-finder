from django.db import models
from django.contrib.auth.models import User

class Topic(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.CharField(max_length=256)
    experience_level = models.CharField(max_length=64)
    dedication = models.CharField(max_length=64)

    def __str__(self) -> str:
        return f'{self.user.email}: {self.topic}'

