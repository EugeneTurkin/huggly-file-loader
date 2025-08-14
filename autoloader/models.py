from django.db import models
from django.utils import timezone


class Task(models.Model):
    class TaskType(models.TextChoices):
        UPLOAD = "upload"
    
    class Status(models.TextChoices):
        IN_PROGRESS = "in progress"
        DONE = "done"
        FAILED = "failed"

    owner = models.TextField(default="admin", null=False)
    notification_recipient = models.EmailField(null=False) 
    task_type = models.TextField(choices=TaskType, null=False)
    creation_ts = models.DateTimeField(default=timezone.now)
    status = models.TextField(choices=Status)
    destination = models.CharField(null=False)
    source = models.FilePathField(path="Z:/НА МОСКВУ/test", null=False)
    

    def __str__(self):
        return f"Task by {self.owner}: {self.task_type} {self.source} to {self.destination}"


"""
Task:
    id              1
    owner           admin
    task_type       upload
    destination     yandex?
    source          192.168.1.206/peregon/НА МОСКВУ/test
    creation ts     2025.8.14 00:00:00
    status          IN PROGRESS
"""
