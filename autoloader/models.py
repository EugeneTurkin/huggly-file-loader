from django.db import models
from django.utils import timezone


class Ticket(models.Model):
    link = models.CharField(max_length=256)
    sub_time = models.DateTimeField(default=timezone.now)
    target_dir = models.TextField()  # TODO: enums
    client = models.TextField()
    status = models.TextField(default="2")

    def __str__(self):
        return f"Ticket: from - {self.link}, to {self.target_dir}"
