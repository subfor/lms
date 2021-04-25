web: gunicorn LMS.wsgi --log-file -
worker: celery  -A LMS.celery worker -l info -E -B