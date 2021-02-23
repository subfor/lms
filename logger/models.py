from django.db import models
from django.utils import timezone


class LogRecord(models.Model):
    path = models.CharField(max_length=100, verbose_name='URL')
    method = models.CharField(max_length=10, verbose_name='Method')
    execution_time_sec = models.FloatField()
    access_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.path}  {self.method} {self.execution_time_sec}"
