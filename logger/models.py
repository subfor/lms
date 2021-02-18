from django.db import models


class LogRecord(models.Model):
    path = models.CharField(max_length=100, verbose_name='URL')
    method = models.CharField(max_length=10, verbose_name='Method')
    execution_time_sec = models.FloatField()

    def __str__(self):
        return f"{self.path}  {self.method}"
