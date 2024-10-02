from django.db import models
class Subject(models.Model):
    class ExperienceChoices(models.IntegerChoices):
        NEW = 1, 'I am completely new'
        BASICS = 2, 'I know some basics'
        REFRESH = 3, 'Worked in the past but need to refresh'

    class DedicationChoices(models.IntegerChoices):
        CASUAL = 1, 'I want to learn casually at my own pace'
        DEDICATED = 2, 'I am busy but I have dedicated time for learning'
        FULL_TIME = 3, 'I am a full time learner'

    subject_name = models.CharField(max_length=256)
    experience_code = models.IntegerField(choices=ExperienceChoices.choices)
    dedication_code = models.IntegerField(choices=DedicationChoices.choices)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.subject_name}'
    
    def save(self, *args, **kwargs):
        self.subject_name = ' '.join(self.subject_name.strip().upper().split())
        super().save(*args, **kwargs)

    def get_experience_display(self):
        return self.ExperienceChoices(self.experience_code).label

    def get_dedication_display(self):
        return self.DedicationChoices(self.dedication_code).label

    class Meta:
        unique_together = ('subject_name', 'experience_code', 'dedication_code')

class Topic(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='topics')
    topic_name = models.CharField(max_length=256)
    description = models.CharField(max_length=256)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f''

class YoutubeVideo(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='videos')
    video_key = models.CharField(max_length=32)
    video_title = models.CharField(max_length=256)
    likes_count = models.IntegerField(null=True)
    views_count = models.IntegerField(null=True)
    uploaded_on = models.DateField(null=True)
    created_on = models.DateTimeField(auto_now_add=True)

