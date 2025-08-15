from django.conf import settings
from django.db import models
from django.utils import timezone


class Task(models.Model):
    class Meta:
        abstract = True
    
    class Action(models.TextChoices):
        UPLOAD = "загрузка"

    class Status(models.TextChoices):
        IN_PROGRESS = "выполняется"
        DONE = "завершен"
        FAILED = "ошибка"

    owner = models.TextField(default="admin", null=False)
    action = models.TextField(choices=Action, null=False)
    creation_ts = models.DateTimeField(default=timezone.now)
    
    # Fields to be displayed by a form
    notification_recipient = models.EmailField(null=False) 
    status = models.TextField(choices=Status)

    # Fields to be rewritten by child classes
    destination = models.CharField(null=False)
    source = models.TextField(null=False)
    

    def __str__(self):
        return f"Задача от {self.owner}: {self.action} файла {self.source} в {self.destination}"


class UploadTask(Task):
    class Destination(models.TextChoices):
        YANDEX = "файлообменник (яндекс)"
        
    destination = models.TextField(choices=Destination, null=False)
    source = models.FilePathField(path=settings.STORAGE_DIR, null=False)
