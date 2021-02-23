# from datetime import datetime, timedelta

from celery import shared_task


from logger.models import LogRecord


@shared_task
def delete_logs():
    # LogRecord.objects.filter(access_time__lte=datetime.now() - timedelta(days=1)).delete()
    LogRecord.objects.all().delete()