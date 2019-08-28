web: gunicorn toolscensus.wsgi --log-file - --reload
worker: celery worker --app=toolscensus.celery.app
