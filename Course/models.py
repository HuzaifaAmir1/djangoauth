from django.db import models
from django.conf import settings


class Course(models.Model):
    title = models.CharField(max_length=100)
    def __str__(self):
        return self.title

class Video(models.Model):
    title = models.CharField(max_length=100)
    file = models.FileField(upload_to='videos/')
    course = models.ForeignKey(Course, related_name='videos', on_delete=models.CASCADE)
    def __str__(self):
        return self.title

class UserProgress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='progress', on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    watched = models.BooleanField(default=False)
