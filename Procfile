web: gunicorn LMS.wsgi --log-file -
worker: celery -A -A LMS worker -l info -E -B