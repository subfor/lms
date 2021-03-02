from django.contrib import admin

# Register your models here.
from exchanger.models import ExchangeRate

admin.site.register(ExchangeRate)