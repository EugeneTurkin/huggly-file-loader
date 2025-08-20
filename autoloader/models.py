from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Task(models.Model):
    class Meta:
        abstract = True
    
    class Action(models.TextChoices):
        UPLOAD = "загрузка"

    class Status(models.TextChoices):
        IN_PROGRESS = "in progress", _("в процессе")
        DONE = "done", _("завершено")
        FAILED = "failed", _("неудачно")

    owner = models.TextField(default="admin", null=False)
    action = models.TextField(choices=Action, null=False)
    creation_ts = models.DateTimeField(default=timezone.now)
    notification_recipient = models.EmailField(verbose_name="Почта, куда направить уведомление", null=False) 
    status = models.TextField(choices=Status, default=Status.IN_PROGRESS)
    destination = models.CharField(null=False)
    source = models.TextField(null=False)
    file_rename = models.CharField(verbose_name="Как назвать файл? (Оставьте пустым чтобы сохранить исходное имя)",
                                   max_length=128, null=True, blank=True)

    def __str__(self):
        return f"Задача от {self.owner}: {self.action} файла {self.source} в {self.destination}"


class UploadTask(Task):
    class Destination(models.TextChoices):
        YANDEX = "yandex", _("файлообменник (яндекс)")
        
    destination = models.TextField(verbose_name="Куда загрузить", choices=Destination, null=False)
    source = models.FilePathField(verbose_name="Выберите файл", path=settings.STORAGE_DIR, null=False)
