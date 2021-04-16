web: gunicorn LMS.wsgi --log-file -
worker: celery -A LMS.celery worker --beat