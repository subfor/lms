from bulk_update_or_create import BulkUpdateOrCreateQuerySet

from django.db import models
from django.utils import timezone


class ExchangeRate(models.Model):
    objects = BulkUpdateOrCreateQuerySet.as_manager()
    cur_id = models.AutoField(primary_key=True)
    currency = models.CharField(max_length=3, unique=True)
    buy = models.DecimalField(max_digits=8, decimal_places=3)
    buy_status = models.IntegerField()
    sell = models.DecimalField(max_digits=8, decimal_places=3)
    sell_status = models.IntegerField()
    created = models.DateTimeField(default=timezone.now)

    # def __str__(self):
    #     return f"{self.currency} {self.buy} {self.buy_status} {self.sell} {self.sell_status} {self.created}"
