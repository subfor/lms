from decimal import Decimal

from celery import shared_task

from exchanger.models import ExchangeRate

import requests


def get_rate():
    url = "https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5"
    r = requests.get(url, timeout=None)
    rates = r.json()
    return rates[:3]


def get_status(currency: str, operation_name: str, current_rate: str):
    status = ExchangeRate.objects.filter(currency=currency).all()
    if status.exists():
        # rate_in_db = BulkUpdateOrCreateQuerySet.values(status, operation_name)[0][operation_name]
        rate_in_db = status.values()[0][operation_name]
        if rate_in_db == Decimal(current_rate):
            return 0
        elif rate_in_db < Decimal(current_rate):
            return 1
        elif rate_in_db > Decimal(current_rate):
            return 2
    return 0


def write_to_db(rates: dict):
    items_rate = [
        ExchangeRate(currency=rate['ccy'],
                     buy=rate['buy'],
                     buy_status=get_status(rate['ccy'], 'buy', rate['buy']),
                     sell=rate['sale'],
                     sell_status=get_status(rate['ccy'], 'sell', rate['sale']),
                     )
        for rate in rates
    ]

    ExchangeRate.objects.bulk_update_or_create(items_rate, ['currency',
                                                            'buy',
                                                            'buy_status',
                                                            'sell',
                                                            'sell_status',
                                                            'created'
                                                            ], match_field='currency')


@shared_task
def write_currency():
    write_to_db(get_rate())
